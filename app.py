"""
期现交易策略汇报软件 - 主应用（支持云端部署）
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
import os
import sqlite3
from datetime import datetime, timedelta
import json
from config import Config
from db_manager import db_manager
from modules.data_processor import DataProcessor
from modules.report_generator import ReportGenerator
from modules.strategy_manager import StrategyManager

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

# 添加缓存控制 - 禁用模板缓存
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(response):
    """添加缓存控制头"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化数据库
def init_db():
    """初始化数据库 - 自动适配本地 SQLite 或云端 PostgreSQL"""
    db_manager.init_db()

# 数据库连接辅助函数
def get_db_connection():
    """获取数据库连接 - 自动适配云端/本地"""
    return db_manager.get_connection()

# 主页
@app.route('/')
def index():
    return render_template('index.html')

# 数据上传页面
@app.route('/upload')
def upload():
    return render_template('upload.html')

# 策略管理页面
@app.route('/strategies')
def strategies():
    return render_template('strategies.html')

# 执行汇总页面
@app.route('/summary')
def summary():
    return render_template('summary.html')

# 策略汇报页面
@app.route('/report')
def report():
    return render_template('report.html')

# 主力合约配置页面
@app.route('/main-contracts')
def main_contracts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM main_contracts ORDER BY effective_date DESC')
    contracts = cursor.fetchall()
    conn.close()
    return render_template('main_contracts.html', contracts=contracts)

# 处理数据上传
@app.route('/api/upload', methods=['POST'])
def handle_upload():
    try:
        file_type = request.form.get('file_type')
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': '没有选择文件'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': '文件名为空'})
        
        if file:
            filename = f"{file_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # 保存到数据库
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO data_files (file_type, file_name, file_path) VALUES (?, ?, ?)',
                (file_type, file.filename, filepath)
            )
            conn.commit()
            conn.close()
            
            # 处理数据
            processor = DataProcessor()
            result = processor.process_file(file_type, filepath)
            
            return jsonify({'success': True, 'message': '上传成功', 'data': result})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API: 获取策略列表
@app.route('/api/strategies')
def get_strategies():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM strategies ORDER BY sort_order, id')
    columns = [description[0] for description in cursor.description]
    strategies = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'data': strategies})

# API: 添加/更新策略
@app.route('/api/strategies', methods=['POST'])
def save_strategy():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if data.get('id'):
            # 更新
            cursor.execute('''
                UPDATE strategies SET
                    strategy_code = ?, strategy_name = ?, strategy_type = ?, business_type = ?,
                    futures_contract = ?, futures_contract2 = ?, spot_variety = ?, forward_variety = ?,
                    futures_direction = ?, spot_direction = ?, plan_quantity = ?,
                    apply_org = ?, apply_person = ?, apply_date = ?, valid_until = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (
                data['strategy_code'], data['strategy_name'], data['strategy_type'], data['business_type'],
                data.get('futures_contract'), data.get('futures_contract2'), data.get('spot_variety'), data.get('forward_variety'),
                data.get('futures_direction'), data.get('spot_direction'), data.get('plan_quantity'),
                data.get('apply_org'), data.get('apply_person'), data.get('apply_date'), data.get('valid_until'),
                data['id']
            ))
        else:
            # 新增
            cursor.execute('''
                INSERT INTO strategies (
                    strategy_code, strategy_name, strategy_type, business_type,
                    futures_contract, futures_contract2, spot_variety, forward_variety,
                    futures_direction, spot_direction, plan_quantity,
                    apply_org, apply_person, apply_date, valid_until
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['strategy_code'], data['strategy_name'], data['strategy_type'], data['business_type'],
                data.get('futures_contract'), data.get('futures_contract2'), data.get('spot_variety'), data.get('forward_variety'),
                data.get('futures_direction'), data.get('spot_direction'), data.get('plan_quantity'),
                data.get('apply_org'), data.get('apply_person'), data.get('apply_date'), data.get('valid_until')
            ))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': '保存成功'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API: 删除策略
@app.route('/api/strategies/<int:strategy_id>', methods=['DELETE'])
def delete_strategy(strategy_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM strategies WHERE id = ?', (strategy_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API: 更新策略排序
@app.route('/api/strategies/reorder', methods=['POST'])
def reorder_strategies():
    try:
        data = request.json
        orders = data.get('orders', [])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for order in orders:
            cursor.execute(
                'UPDATE strategies SET sort_order = ? WHERE id = ?',
                (order['sort_order'], order['id'])
            )
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': '排序更新成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API: 获取策略汇总数据
@app.route('/api/summary')
def get_summary():
    try:
        manager = StrategyManager()
        data = manager.get_summary_data()
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API: 获取策略按周复盘数据
@app.route('/api/strategy/<int:strategy_id>/weekly')
def get_strategy_weekly(strategy_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取策略信息
        cursor.execute('SELECT * FROM strategies WHERE id = ?', (strategy_id,))
        columns = [description[0] for description in cursor.description]
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return jsonify({'success': False, 'error': '策略不存在'})
        
        strategy = dict(zip(columns, row))
        conn.close()
        
        # 获取按周数据
        manager = StrategyManager()
        weekly_data = manager.get_strategy_weekly_data(strategy)
        
        return jsonify({'success': True, 'data': weekly_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API: 获取策略基差数据
@app.route('/api/strategy/<int:strategy_id>/basis')
def get_strategy_basis(strategy_id):
    try:
        from modules.basis_chart import BasisChartCalculator
        
        # 获取策略信息
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM strategies WHERE id = ?', (strategy_id,))
        columns = [description[0] for description in cursor.description]
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'success': False, 'error': '策略不存在'})
        
        strategy = dict(zip(columns, row))
        
        # 计算基差数据
        calculator = BasisChartCalculator()
        data = calculator.get_basis_data(strategy)
        
        # 确定时间范围描述
        futures_contract = strategy.get('futures_contract', '')
        is_main_contract = futures_contract in ['螺纹主链', '热卷主链', 'RB主链', 'HC主链']
        time_range = '近1年' if is_main_contract else '近3个月'
        
        return jsonify({
            'success': True, 
            'data': data,
            'time_range': time_range,
            'is_main_contract': is_main_contract
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API: 生成PDF汇报
@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    try:
        data = request.json
        
        # 为每个策略生成基差走势图和获取复盘数据
        from modules.basis_chart_generator import BasisChartGenerator
        from modules.strategy_manager import StrategyManager
        chart_gen = BasisChartGenerator()
        strategy_manager = StrategyManager()
        
        chart_images = {}
        strategies = data.get('strategies', [])
        
        # 优化：一次性获取所有策略的复盘数据和汇总数据
        all_weekly_data = strategy_manager.get_all_strategies_weekly_data(strategies)
        
        # 连接数据库获取策略分析
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for strategy in strategies:
            strategy_id = strategy['id']
            
            # 生成基差走势图
            chart_path = os.path.join(app.config['UPLOAD_FOLDER'], f"basis_chart_{strategy_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
            if chart_gen.generate_basis_chart(strategy, chart_path):
                chart_images[strategy_id] = chart_path
            
            # 获取策略复盘数据（已预计算）
            strategy['weekly_data'] = all_weekly_data.get(strategy_id, [])
            
            # 获取策略汇总数据（持仓/平仓数量和盈亏）
            summary = strategy_manager.calculate_strategy_summary(strategy)
            strategy['position_quantity'] = summary['position_quantity']
            strategy['position_profit'] = summary['position_profit']
            strategy['close_quantity'] = summary['close_quantity']
            strategy['close_profit'] = summary['close_profit']
            
            # 获取策略分析数据
            cursor.execute('SELECT operation_scale, operation_direction, core_logic, risk_response FROM strategy_analysis WHERE strategy_id = ?', (strategy_id,))
            analysis_row = cursor.fetchone()
            if analysis_row:
                strategy['analysis'] = {
                    'operation_scale': analysis_row[0] or '',
                    'operation_direction': analysis_row[1] or '',
                    'core_logic': analysis_row[2] or '',
                    'risk_response': analysis_row[3] or ''
                }
            else:
                strategy['analysis'] = {}
        
        conn.close()
        
        # 生成PDF
        report_gen = ReportGenerator()
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
        report_gen.generate_pdf(data, output_path, chart_images)
        
        return jsonify({
            'success': True,
            'message': '生成成功',
            'download_url': f'/download/{os.path.basename(output_path)}'
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})

# API: 获取仪表板数据
@app.route('/api/dashboard')
def get_dashboard():
    try:
        import openpyxl
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取各类型数据文件并统计行数
        def count_excel_rows(file_type, header_rows=1):
            cursor.execute(
                "SELECT file_path FROM data_files WHERE file_type = ? ORDER BY upload_date DESC LIMIT 1",
                (file_type,)
            )
            result = cursor.fetchone()
            if result and os.path.exists(result[0]):
                try:
                    wb = openpyxl.load_workbook(result[0], data_only=True)
                    ws = wb.active
                    # 统计非空行数（减去表头）
                    total_rows = 0
                    for row in ws.iter_rows(min_row=header_rows+1, values_only=True):
                        if any(cell is not None for cell in row):
                            total_rows += 1
                    return total_rows
                except:
                    return 0
            return 0
        
        spot_count = count_excel_rows('spot_price', 1)
        futures_count = count_excel_rows('futures_price', 1)
        trade_count = count_excel_rows('trade_record', 2)  # 交易记录有2行表头
        
        cursor.execute("SELECT COUNT(*) FROM strategies")
        strategy_count = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'spot_count': spot_count,
                'futures_count': futures_count,
                'trade_count': trade_count,
                'strategy_count': strategy_count
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# 下载文件
@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)

# 预览PDF文件（浏览器内嵌查看）
@app.route('/preview/<filename>')
def preview_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=False, mimetype='application/pdf')

# API: 获取主力合约列表
@app.route('/api/main-contracts', methods=['GET'])
def get_main_contracts():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, variety, contract_code, effective_date, expiry_date 
            FROM main_contracts 
            ORDER BY effective_date DESC
        ''')
        
        columns = [description[0] for description in cursor.description]
        contracts = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return jsonify({'success': True, 'data': contracts})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API: 保存主力合约
@app.route('/api/main-contracts', methods=['POST'])
def save_main_contract():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO main_contracts (variety, contract_code, effective_date, expiry_date)
            VALUES (?, ?, ?, ?)
        ''', (data['variety'], data['contract_code'], data['effective_date'], data['expiry_date']))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': '保存成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API: 获取策略分析
@app.route('/api/strategy/<int:strategy_id>/analysis', methods=['GET'])
def get_strategy_analysis(strategy_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM strategy_analysis WHERE strategy_id = ?
        ''', (strategy_id,))
        
        columns = [description[0] for description in cursor.description]
        row = cursor.fetchone()
        conn.close()
        
        if row:
            analysis = dict(zip(columns, row))
            return jsonify({'success': True, 'data': analysis})
        else:
            # 返回空数据
            return jsonify({
                'success': True, 
                'data': {
                    'operation_scale': '',
                    'operation_direction': '',
                    'core_logic': '',
                    'execution_plan': '',
                    'risk_response': ''
                }
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API: 保存策略分析
@app.route('/api/strategy/<int:strategy_id>/analysis', methods=['POST'])
def save_strategy_analysis(strategy_id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查是否已存在
        cursor.execute('SELECT id FROM strategy_analysis WHERE strategy_id = ?', (strategy_id,))
        existing = cursor.fetchone()
        
        if existing:
            # 更新
            cursor.execute('''
                UPDATE strategy_analysis SET
                    operation_scale = ?,
                    operation_direction = ?,
                    core_logic = ?,
                    execution_plan = ?,
                    risk_response = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE strategy_id = ?
            ''', (
                data.get('operation_scale', ''),
                data.get('operation_direction', ''),
                data.get('core_logic', ''),
                data.get('execution_plan', ''),
                data.get('risk_response', ''),
                strategy_id
            ))
        else:
            # 插入
            cursor.execute('''
                INSERT INTO strategy_analysis 
                (strategy_id, operation_scale, operation_direction, core_logic, execution_plan, risk_response)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                strategy_id,
                data.get('operation_scale', ''),
                data.get('operation_direction', ''),
                data.get('core_logic', ''),
                data.get('execution_plan', ''),
                data.get('risk_response', '')
            ))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': '保存成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    init_db()
    # 设置UTF-8编码
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    app.run(debug=True, port=5000, host='0.0.0.0')


# Vercel 入口
app = app

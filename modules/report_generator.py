# -*- coding: utf-8 -*-
"""
PDF报告生成器 - 生成专业级策略汇报

目录结构：
一、行情回顾
二、行情展望
三、策略执行情况汇总
四、策略详情（每个策略一页）
五、关键点位

每部分一页A4纸（除第四部分外）
第四部分每页策略包含：基本要素、基差走势图、策略复盘、策略分析
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self):
        self.setup_fonts()
        self.styles = self.create_styles()
    
    def setup_fonts(self):
        """设置中文字体 - 支持Windows和Linux"""
        # 默认使用英文字体
        self.font_name = 'Helvetica'
        self.font_name_bold = 'Helvetica-Bold'
        
        # Windows字体路径
        windows_fonts = [
            ('C:/Windows/Fonts/simhei.ttf', 'SimHei'),
            ('C:/Windows/Fonts/simkai.ttf', 'SimKai'),
            ('C:/Windows/Fonts/simsun.ttc', 'SimSun'),
            ('C:/Windows/Fonts/msyh.ttc', 'MicrosoftYaHei'),
            ('C:/Windows/Fonts/msyhbd.ttc', 'MicrosoftYaHei-Bold'),
        ]
        
        # Linux字体路径（PythonAnywhere等云端环境）
        linux_fonts = [
            ('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 'WenQuanYiZenHei'),
            ('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 'WenQuanYiMicroHei'),
            ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'DejaVuSans'),
            ('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 'LiberationSans'),
        ]
        
        # 检查系统类型并选择合适的字体列表
        import platform
        if platform.system() == 'Windows':
            font_paths = windows_fonts
        else:
            font_paths = linux_fonts
        
        registered = []
        for font_path, font_name in font_paths:
            if os.path.exists(font_path):
                try:
                    # 检查字体是否已注册
                    if font_name not in pdfmetrics.getRegisteredFontNames():
                        pdfmetrics.registerFont(TTFont(font_name, font_path))
                    registered.append(font_name)
                    print(f"成功注册字体: {font_name}")
                except Exception as e:
                    print(f"注册字体 {font_name} 失败: {e}")
        
        # 优先级设置
        priority = ['SimHei', 'SimKai', 'SimSun', 'MicrosoftYaHei', 
                   'WenQuanYiZenHei', 'WenQuanYiMicroHei', 'DejaVuSans', 'LiberationSans']
        
        for font in priority:
            if font in registered:
                self.font_name = font
                self.font_name_bold = font
                print(f"使用字体: {font}")
                break
        
        # 如果还是没有中文字体，尝试使用项目目录下的备用字体
        if self.font_name == 'Helvetica':
            self._try_use_local_font()
    
    def _try_use_local_font(self):
        """尝试使用项目目录下的备用字体"""
        # 获取项目根目录
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_dir = os.path.join(current_dir, 'static', 'fonts')
        
        # 如果字体目录不存在，尝试创建并下载字体
        if not os.path.exists(font_dir):
            os.makedirs(font_dir, exist_ok=True)
        
        # 检查是否已有字体文件
        local_fonts = [
            (os.path.join(font_dir, 'simhei.ttf'), 'LocalSimHei'),
            (os.path.join(font_dir, 'wqy-zenhei.ttc'), 'LocalWQY'),
        ]
        
        for font_path, font_name in local_fonts:
            if os.path.exists(font_path):
                try:
                    if font_name not in pdfmetrics.getRegisteredFontNames():
                        pdfmetrics.registerFont(TTFont(font_name, font_path))
                    self.font_name = font_name
                    self.font_name_bold = font_name
                    print(f"使用本地字体: {font_name}")
                    return
                except Exception as e:
                    print(f"使用本地字体失败: {e}")
        
        # 如果本地没有字体，尝试从网络下载（仅作为最后的备选）
        print("警告：未找到中文字体，PDF可能显示为方框。建议上传字体文件到 static/fonts 目录。")
    
    def create_styles(self):
        """创建样式"""
        styles = getSampleStyleSheet()
        
        # 标题样式
        styles.add(ParagraphStyle(
            name='ReportTitle',
            fontSize=32,
            leading=40,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.white,
            fontName=self.font_name_bold
        ))
        
        styles.add(ParagraphStyle(
            name='ChapterTitle',
            fontSize=18,
            leading=26,
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=12,
            textColor=colors.black,
            fontName=self.font_name_bold
        ))
        
        styles.add(ParagraphStyle(
            name='SectionTitle',
            fontSize=13,
            leading=18,
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=6,
            textColor=colors.black,
            fontName=self.font_name_bold
        ))
        
        styles.add(ParagraphStyle(
            name='ReportBodyText',
            fontSize=10,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            textColor=colors.HexColor('#1a202c'),
            fontName=self.font_name
        ))
        
        styles.add(ParagraphStyle(
            name='StrategyTitle',
            fontSize=14,
            leading=20,
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=8,
            textColor=colors.HexColor('#1a365d'),
            fontName=self.font_name_bold
        ))
        
        return styles
    
    def generate_pdf(self, data, output_path, chart_images=None):
        """
        生成PDF报告 - 横向A4布局
        
        Args:
            data: 报告数据
            output_path: 输出路径
            chart_images: 策略ID到基差走势图路径的字典
        """
        # 横向A4设置
        doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(A4),
            rightMargin=10*mm,
            leftMargin=10*mm,
            topMargin=10*mm,
            bottomMargin=10*mm
        )
        
        story = []
        
        # 第1页：封面
        self.add_cover_page(story, data)
        
        # 第2页：目录
        story.append(PageBreak())
        self.add_toc_page(story, data)
        
        # 第3页：行情回顾
        story.append(PageBreak())
        self.add_market_review_page(story, data)
        
        # 第4页：行情展望
        story.append(PageBreak())
        self.add_market_outlook_page(story, data)
        
        # 第5页：策略执行情况汇总
        story.append(PageBreak())
        self.add_strategy_summary_page(story, data)
        
        # 第6页起：策略详情（每页一个策略）
        strategies = data.get('strategies', [])
        # 过滤掉非字典类型的策略数据
        strategies = [s for s in strategies if isinstance(s, dict)]
        
        for idx, strategy in enumerate(strategies, 1):
            story.append(PageBreak())
            strategy['page_number'] = idx
            chart_path = chart_images.get(strategy.get('id')) if chart_images else None
            self.add_strategy_detail_page(story, strategy, chart_path)
        
        # 关键点位页
        if strategies:
            story.append(PageBreak())
        self.add_key_levels_page(story, data)
        
        # 尾页
        story.append(PageBreak())
        self.add_ending_page(story, data)
        
        doc.build(story)
    
    def add_cover_page(self, story, data):
        """添加封面页 - 藏青蓝背景，白色字体"""
        # 创建全页背景
        cover_elements = []
        
        # 顶部留白
        cover_elements.append(Spacer(1, 3*cm))
        
        # 第一行：钢晨钢材交易策略 - 放大字体，白色
        title1_style = ParagraphStyle(
            'CoverTitle1',
            fontSize=48,
            leading=56,
            alignment=TA_CENTER,
            textColor=colors.white,
            fontName=self.font_name_bold
        )
        cover_elements.append(Paragraph("钢晨钢材交易策略", title1_style))
        
        cover_elements.append(Spacer(1, 0.3*cm))
        
        # 第二行：执行周报 - 放大字体，白色
        title2_style = ParagraphStyle(
            'CoverTitle2',
            fontSize=48,
            leading=56,
            alignment=TA_CENTER,
            textColor=colors.white,
            fontName=self.font_name_bold
        )
        cover_elements.append(Paragraph("执行周报", title2_style))
        
        cover_elements.append(Spacer(1, 1.5*cm))
        
        # 第三行：第X周 - 只显示阿拉伯数字
        week = data.get('report_week', datetime.now().strftime('%Y年第%W周'))
        # 提取纯数字周数
        week_num = '14'  # 默认
        if 'W' in week:
            try:
                week_num = week.split('W')[-1].split('-')[0] if '-' in week else week.split('W')[-1]
                week_num = ''.join(filter(str.isdigit, week_num))
            except:
                pass
        elif '第' in week:
            try:
                week_num = ''.join(filter(str.isdigit, week.split('第')[-1].split('周')[0]))
            except:
                pass
        
        week_style = ParagraphStyle(
            'CoverWeek',
            fontSize=42,
            leading=50,
            alignment=TA_CENTER,
            textColor=colors.white,
            fontName=self.font_name_bold
        )
        cover_elements.append(Paragraph(f"第{week_num}周", week_style))
        
        cover_elements.append(Spacer(1, 2.5*cm))
        
        # 副标题 - 白色
        subtitle_style = ParagraphStyle(
            'CoverSubtitle',
            fontSize=16,
            leading=24,
            alignment=TA_CENTER,
            textColor=colors.white,
            fontName=self.font_name
        )
        cover_elements.append(Paragraph("Strategy Execution Weekly Report", subtitle_style))
        
        cover_elements.append(Spacer(1, 2.5*cm))
        
        # 生成日期 - 白色
        date_style = ParagraphStyle(
            'CoverDate',
            fontSize=14,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors.white,
            fontName=self.font_name
        )
        cover_elements.append(Paragraph(f"生成日期：{datetime.now().strftime('%Y年%m月%d日')}", date_style))
        
        cover_elements.append(Spacer(1, 0.8*cm))
        
        # 编制信息 - 白色
        info_style = ParagraphStyle(
            'CoverInfo',
            fontSize=14,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors.white,
            fontName=self.font_name
        )
        dept_text = f"编制部门：{data.get('department', '经营管理部')}"
        cover_elements.append(Paragraph(dept_text, info_style))
        
        # 放入表格实现页面布局 - 藏青蓝背景，填满整个页面
        # A4横向: 297x210mm, 边距10mm, 可用: 277x190mm
        cover_table = Table([[cover_elements]], colWidths=[27.5*cm], rowHeights=[18.5*cm])
        cover_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a365d')),  # 藏青蓝
        ]))
        
        story.append(cover_table)
    
    def add_toc_page(self, story, data):
        """添加目录页"""
        title = Paragraph("目  录", self.styles['ChapterTitle'])
        story.append(title)
        
        story.append(Spacer(1, 1*cm))
        
        strategy_count = len(data.get('strategies', []))
        start_page = 6  # 策略详情从第6页开始
        
        toc_items = [
            ('一、', '行情回顾', '3'),
            ('二、', '行情展望', '4'),
            ('三、', '策略执行情况汇总', '5'),
            ('四、', '策略详情', f'{start_page}-{start_page + strategy_count - 1}'),
            ('五、', '关键点位', str(start_page + strategy_count)),
        ]
        
        for prefix, name, page in toc_items:
            toc_data = [[f'{prefix}{name}', page]]
            toc_table = Table(toc_data, colWidths=[22*cm, 3*cm])
            toc_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, 0), self.font_name_bold),
                ('FONTNAME', (1, 0), (1, 0), self.font_name),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
                ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor('#e2e8f0')),
            ]))
            story.append(toc_table)
    
    def add_market_review_page(self, story, data):
        """添加行情回顾页"""
        title = Paragraph("一、行情回顾", self.styles['ChapterTitle'])
        story.append(title)
        
        story.append(Spacer(1, 0.3*cm))
        
        # 价格走势
        story.append(Paragraph("（一）价格走势", self.styles['SectionTitle']))
        price_text = data.get('price_trend', '本周螺纹钢期货主力合约价格呈现震荡走势...')
        story.append(Paragraph(price_text, self.styles['ReportBodyText']))
        
        # 产量情况
        story.append(Paragraph("（二）产量情况", self.styles['SectionTitle']))
        production_text = data.get('production_status', '本周全国主要钢厂螺纹钢产量...')
        story.append(Paragraph(production_text, self.styles['ReportBodyText']))
        
        # 需求情况
        story.append(Paragraph("（三）需求情况", self.styles['SectionTitle']))
        demand_text = data.get('demand_status', '本周市场成交活跃度...')
        story.append(Paragraph(demand_text, self.styles['ReportBodyText']))
        
        # 库存情况
        story.append(Paragraph("（四）库存情况", self.styles['SectionTitle']))
        inventory_text = data.get('inventory_status', '本周社会库存和钢厂库存...')
        story.append(Paragraph(inventory_text, self.styles['ReportBodyText']))
    
    def add_market_outlook_page(self, story, data):
        """添加行情展望页"""
        title = Paragraph("二、行情展望", self.styles['ChapterTitle'])
        story.append(title)
        
        story.append(Spacer(1, 0.3*cm))
        
        # 宏观方面
        story.append(Paragraph("（一）宏观方面", self.styles['SectionTitle']))
        macro_text = data.get('macro_outlook', '宏观政策持续发力...')
        story.append(Paragraph(macro_text, self.styles['ReportBodyText']))
        
        # 成本方面
        story.append(Paragraph("（二）成本方面", self.styles['SectionTitle']))
        cost_text = data.get('cost_outlook', '原材料成本支撑...')
        story.append(Paragraph(cost_text, self.styles['ReportBodyText']))
        
        # 技术方面
        story.append(Paragraph("（三）技术方面", self.styles['SectionTitle']))
        tech_text = data.get('technical_outlook', '技术指标显示...')
        story.append(Paragraph(tech_text, self.styles['ReportBodyText']))
        
        # 市场观点
        story.append(Paragraph("（四）市场观点", self.styles['SectionTitle']))
        view_text = data.get('market_view', '综合来看，短期市场预计...')
        story.append(Paragraph(view_text, self.styles['ReportBodyText']))
    
    def add_strategy_summary_page(self, story, data):
        """添加策略执行情况汇总页"""
        title = Paragraph("三、策略执行情况汇总", self.styles['ChapterTitle'])
        story.append(title)
        
        story.append(Spacer(1, 0.5*cm))
        
        # 表头
        headers = ['策略编号', '策略名称', '计划数量(吨)', '持仓数量(吨)', '持仓盈亏(元)', '平仓数量(吨)', '平仓盈亏(元)']
        
        strategies = data.get('strategies', [])
        # 过滤掉非字典类型的策略数据
        strategies = [s for s in strategies if isinstance(s, dict)]
        
        table_data = [headers]
        
        for s in strategies:
            row = [
                s.get('strategy_code', ''),
                s.get('strategy_name', ''),
                str(s.get('plan_quantity', '')),
                str(s.get('position_quantity', '')),
                f"{s.get('position_profit', 0):,.2f}" if s.get('position_profit') else '',
                str(s.get('close_quantity', '')),
                f"{s.get('close_profit', 0):,.2f}" if s.get('close_profit') else '',
            ]
            table_data.append(row)
        
        # 创建表格（适应横向A4纸，总宽度约27cm）
        col_widths = [4*cm, 6*cm, 3*cm, 3*cm, 3.5*cm, 3*cm, 3.5*cm]
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), self.font_name_bold),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            
            ('FONTNAME', (0, 1), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 1), (1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
            
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(table)
    
    def add_strategy_detail_page(self, story, strategy, chart_path=None):
        """添加单个策略详情页 - 严格一页A4横向布局"""
        # 确保策略是字典类型
        if not isinstance(strategy, dict):
            print(f"警告: 策略数据格式错误: {type(strategy)}")
            strategy = {}
        
        page_num = strategy.get('page_number', 1)
        
        # 策略标题 - 减小字号
        title_text = f"四、策略详情 ({page_num}) {strategy.get('strategy_code', '')}"
        title_style = ParagraphStyle(
            'StrategyDetailTitle',
            fontSize=14,
            leading=18,
            alignment=TA_LEFT,
            spaceBefore=5,
            spaceAfter=5,
            textColor=colors.black,
            fontName=self.font_name_bold
        )
        story.append(Paragraph(title_text, title_style))
        
        # 策略名称
        name_style = ParagraphStyle(
            'StrategyDetailName',
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            spaceBefore=2,
            spaceAfter=5,
            textColor=colors.black,
            fontName=self.font_name_bold
        )
        story.append(Paragraph(strategy.get('strategy_name', ''), name_style))
        
        # （一）基差走势图 - 放在最上面，拉长
        story.append(Paragraph("（一）基差走势图", self.styles['SectionTitle']))
        
        # 读取当前基差值
        current_basis_value = None
        if chart_path:
            basis_text_path = chart_path.replace('.png', '_basis.txt')
            if os.path.exists(basis_text_path):
                try:
                    with open(basis_text_path, 'r', encoding='utf-8') as f:
                        current_basis_value = f.read().strip()
                except:
                    pass
        
        # 显示当前基差值（图外）
        if current_basis_value:
            basis_info_style = ParagraphStyle(
                'BasisInfo',
                fontSize=10,
                leading=14,
                alignment=TA_RIGHT,
                textColor=colors.HexColor('#d32f2f'),
                fontName=self.font_name_bold
            )
            story.append(Paragraph(f"当前基差：{current_basis_value} 元/吨", basis_info_style))
        
        if chart_path and os.path.exists(chart_path):
            # 插入基差走势图 - 宽度最大化，高度适中（去掉标题后减小高度）
            img = Image(chart_path, width=25*cm, height=4*cm)
            story.append(img)
        else:
            story.append(Paragraph("[基差走势图生成中...]", self.styles['ReportBodyText']))
        
        story.append(Spacer(1, 0.2*cm))
        
        # （二）基本要素 与 （三）策略复盘 并排 - 各自独立标题
        # 创建并排标题行 - 调整列宽使标题对齐
        left_title = Paragraph("（二）基本要素", self.styles['SectionTitle'])
        right_title = Paragraph("（三）策略复盘", self.styles['SectionTitle'])
        title_row = Table([[left_title, right_title]], colWidths=[14.5*cm, 12*cm])
        title_row.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(title_row)
        story.append(Spacer(1, 0.1*cm))
        
        # 左侧：基本要素（更紧凑的布局）
        basic_data = [
            ['策略类型', strategy.get('strategy_type', ''), '业务类型', strategy.get('business_type', '')],
            ['期货合约', strategy.get('futures_contract', ''), '期货方向', strategy.get('futures_direction', '')],
            ['现货品种', strategy.get('spot_variety', ''), '现货方向', strategy.get('spot_direction', '')],
            ['计划数量(吨)', str(strategy.get('plan_quantity', '')), '当前基差', str(strategy.get('current_basis', ''))],
        ]
        
        # 缩小基本要素表格宽度，更紧凑 - 调整列宽
        basic_table = Table(basic_data, colWidths=[2.5*cm, 3.8*cm, 2.5*cm, 3.8*cm])
        basic_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), self.font_name_bold),
            ('FONTNAME', (1, 0), (1, -1), self.font_name),
            ('FONTNAME', (2, 0), (2, -1), self.font_name_bold),
            ('FONTNAME', (3, 0), (3, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#edf2f7')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#edf2f7')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        # 右侧：策略复盘
        weekly_data = strategy.get('weekly_data', [])
        if not weekly_data:
            weekly_data = [
                {'week': '第1周', 'open_tons': 0, 'close_tons': 0, 'close_pnl': 0, 'cumulative_tons': 0, 'position_pnl': 0},
            ]
        
        total_open = sum(w.get('open_tons', 0) for w in weekly_data)
        total_close = sum(w.get('close_tons', 0) for w in weekly_data)
        final_position = weekly_data[-1].get('cumulative_tons', 0) if weekly_data else 0
        
        review_headers = ['复盘', '建仓(吨)', '平仓(吨)', '持仓(吨)']
        review_rows = []
        for w in weekly_data:
            review_rows.append([
                w.get('week', ''),
                f"{w.get('open_tons', 0):,.0f}" if w.get('open_tons') else '-',
                f"{w.get('close_tons', 0):,.0f}" if w.get('close_tons') else '-',
                f"{w.get('cumulative_tons', 0):,.0f}"
            ])
        review_rows.append(['合计', f"{total_open:,.0f}", f"{total_close:,.0f}", f"{final_position:,.0f}"])
        
        review_data = [review_headers] + review_rows
        
        review_table = Table(review_data, colWidths=[3.5*cm, 2.8*cm, 2.8*cm, 2.8*cm])
        review_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), self.font_name_bold),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 1), (-1, -2), self.font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#fff8e1')),
            ('FONTNAME', (0, -1), (-1, -1), self.font_name_bold),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        # 并排布局：基本要素 + 策略复盘
        top_row_data = [[basic_table, review_table]]
        top_row_table = Table(top_row_data, colWidths=[14.5*cm, 13*cm])
        top_row_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(top_row_table)
        
        story.append(Spacer(1, 0.15*cm))
        
        # （四）策略分析 - 单独展示，占满宽度
        story.append(Paragraph("（四）策略分析", self.styles['SectionTitle']))
        
        analysis = strategy.get('analysis', {})
        analysis_items = [
            ('操作规模：', analysis.get('operation_scale', '根据市场情况灵活调整仓位')),
            ('操作方向：', analysis.get('operation_direction', '基于基差变化趋势进行套保操作')),
            ('核心逻辑：', analysis.get('core_logic', '利用期现价差进行风险对冲')),
            ('风险应对：', analysis.get('risk_response', '设定止损线，控制最大回撤')),
        ]
        
        analysis_data = []
        for label, content in analysis_items:
            analysis_data.append([
                Paragraph(f"<b>{label}</b>", self.styles['ReportBodyText']),
                Paragraph(content, self.styles['ReportBodyText'])
            ])
        
        analysis_table = Table(analysis_data, colWidths=[3*cm, 23*cm])
        analysis_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(analysis_table)
    
    def _parse_key_levels(self, text, default1, default2, default3, is_resistance=False):
        """从文本中解析关键点位数值
        
        支持的格式：
        支撑位：3100、3050、3000
        压力位：3200、3250、3300
        """
        import re
        
        if not text:
            return default1, default2, default3
        
        # 根据类型确定关键字
        keyword = '压力' if is_resistance else '支撑'
        
        # 查找包含关键字的行
        lines = text.replace('，', ',').replace('、', ',').split('\n')
        for line in lines:
            if keyword in line:
                # 提取所有数字
                numbers = re.findall(r'\d+', line)
                if len(numbers) >= 3:
                    return numbers[0], numbers[1], numbers[2]
                elif len(numbers) == 2:
                    return numbers[0], numbers[1], default3
                elif len(numbers) == 1:
                    return numbers[0], default2, default3
        
        # 如果没找到指定类型的数据，尝试从整个文本中提取数字
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 3:
            if is_resistance:
                # 压力位通常取后三个数字（如果总数>=6，取第4-6个）
                if len(numbers) >= 6:
                    return numbers[3], numbers[4], numbers[5]
                else:
                    return numbers[0], numbers[1], numbers[2]
            else:
                # 支撑位通常取前三个数字
                return numbers[0], numbers[1], numbers[2]
        elif len(numbers) == 2:
            return numbers[0], numbers[1], default3
        elif len(numbers) == 1:
            return numbers[0], default2, default3
        
        return default1, default2, default3

    def add_key_levels_page(self, story, data):
        """添加关键点位页"""
        title = Paragraph("五、关键点位", self.styles['ChapterTitle'])
        story.append(title)
        
        story.append(Spacer(1, 0.5*cm))
        
        # 螺纹钢关键点位
        story.append(Paragraph("（一）螺纹钢主力合约关键点位", self.styles['SectionTitle']))
        
        rb_levels = data.get('rb_key_levels', {})
        # 如果是字符串，解析文本内容
        if isinstance(rb_levels, str):
            rb_s1, rb_s2, rb_s3 = self._parse_key_levels(rb_levels, '3100', '3050', '3000')
            rb_r1, rb_r2, rb_r3 = self._parse_key_levels(rb_levels, '3200', '3250', '3300', is_resistance=True)
        else:
            rb_s1 = rb_levels.get('support1', '3100')
            rb_s2 = rb_levels.get('support2', '3050')
            rb_s3 = rb_levels.get('support3', '3000')
            rb_r1 = rb_levels.get('resistance1', '3200')
            rb_r2 = rb_levels.get('resistance2', '3250')
            rb_r3 = rb_levels.get('resistance3', '3300')
        
        rb_data = [
            ['支撑位', rb_s1, rb_s2, rb_s3],
            ['压力位', rb_r1, rb_r2, rb_r3],
        ]
        
        rb_table = Table(rb_data, colWidths=[5*cm, 7*cm, 7*cm, 7*cm])
        rb_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#edf2f7')),
            ('FONTNAME', (0, 0), (0, -1), self.font_name_bold),
            ('FONTNAME', (1, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(rb_table)
        
        story.append(Spacer(1, 0.5*cm))
        
        # 热卷关键点位
        story.append(Paragraph("（二）热卷主力合约关键点位", self.styles['SectionTitle']))
        
        hc_levels = data.get('hc_key_levels', {})
        # 如果是字符串，解析文本内容
        if isinstance(hc_levels, str):
            hc_s1, hc_s2, hc_s3 = self._parse_key_levels(hc_levels, '3300', '3250', '3200')
            hc_r1, hc_r2, hc_r3 = self._parse_key_levels(hc_levels, '3400', '3450', '3500', is_resistance=True)
        else:
            hc_s1 = hc_levels.get('support1', '3300')
            hc_s2 = hc_levels.get('support2', '3250')
            hc_s3 = hc_levels.get('support3', '3200')
            hc_r1 = hc_levels.get('resistance1', '3400')
            hc_r2 = hc_levels.get('resistance2', '3450')
            hc_r3 = hc_levels.get('resistance3', '3500')
        
        hc_data = [
            ['支撑位', hc_s1, hc_s2, hc_s3],
            ['压力位', hc_r1, hc_r2, hc_r3],
        ]
        
        hc_table = Table(hc_data, colWidths=[3*cm, 4*cm, 4*cm, 4*cm])
        hc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#edf2f7')),
            ('FONTNAME', (0, 0), (0, -1), self.font_name_bold),
            ('FONTNAME', (1, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(hc_table)

    def add_ending_page(self, story, data):
        """添加尾页 - 藏青蓝背景，白色字体"""
        # 创建全页背景
        ending_elements = []
        
        # 顶部留白
        ending_elements.append(Spacer(1, 5*cm))
        
        # 结束语 - 放大字体，白色
        thanks_style = ParagraphStyle(
            'ThanksText',
            fontSize=36,
            leading=44,
            alignment=TA_CENTER,
            textColor=colors.white,
            fontName=self.font_name_bold
        )
        ending_elements.append(Paragraph("感谢您的阅读", thanks_style))
        
        ending_elements.append(Spacer(1, 1.5*cm))
        
        # 分隔线 - 白色半透明
        line_style = ParagraphStyle(
            'LineStyle',
            fontSize=14,
            leading=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#ffffff'),
            fontName=self.font_name
        )
        ending_elements.append(Paragraph("—" * 50, line_style))
        
        ending_elements.append(Spacer(1, 2*cm))
        
        # 添加钢晨钢材交易策略周报 - 与经营管理部同字号
        company_style = ParagraphStyle(
            'CompanyText',
            fontSize=20,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.white,
            fontName=self.font_name_bold
        )
        ending_elements.append(Paragraph("钢晨钢材交易策略周报", company_style))
        
        ending_elements.append(Spacer(1, 0.8*cm))
        
        # 经营管理部
        ending_elements.append(Paragraph("经营管理部", company_style))
        
        ending_elements.append(Spacer(1, 0.8*cm))
        
        # 报告周期 - 只显示数字
        week = data.get('report_week', datetime.now().strftime('%Y年第%W周'))
        # 提取纯数字周数
        week_num = '14'  # 默认
        if 'W' in week:
            try:
                week_num = week.split('W')[-1].split('-')[0] if '-' in week else week.split('W')[-1]
                week_num = ''.join(filter(str.isdigit, week_num))
            except:
                pass
        elif '第' in week:
            try:
                week_num = ''.join(filter(str.isdigit, week.split('第')[-1].split('周')[0]))
            except:
                pass
        
        week_style = ParagraphStyle(
            'WeekText',
            fontSize=16,
            leading=24,
            alignment=TA_CENTER,
            textColor=colors.white,
            fontName=self.font_name
        )
        ending_elements.append(Paragraph(f"第{week_num}周", week_style))
        
        ending_elements.append(Spacer(1, 3*cm))
        
        # 底部声明 - 白色
        footer_style = ParagraphStyle(
            'FooterText',
            fontSize=12,
            leading=20,
            alignment=TA_CENTER,
            textColor=colors.white,
            fontName=self.font_name
        )
        ending_elements.append(Paragraph("本报告仅供参考，不构成投资建议", footer_style))
        ending_elements.append(Spacer(1, 0.5*cm))
        ending_elements.append(Paragraph("内部资料，请勿外传", footer_style))
        
        # 放入表格实现页面布局 - 藏青蓝背景，填满整个页面
        # A4横向: 297x210mm, 边距10mm, 可用: 277x190mm
        ending_table = Table([[ending_elements]], colWidths=[27.5*cm], rowHeights=[18.5*cm])
        ending_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a365d')),  # 藏青蓝
        ]))
        
        story.append(ending_table)

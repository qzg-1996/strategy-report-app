"""
数据库管理器 - 支持 SQLite 和 PostgreSQL (Supabase)
"""
import os
import sqlite3
from config import Config

# 尝试导入 PostgreSQL 驱动
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

class DatabaseManager:
    """数据库管理器 - 自动适配本地 SQLite 和云端 PostgreSQL"""
    
    def __init__(self):
        self.is_postgres = Config.get_db_connection_string().startswith('postgresql')
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'strategy.db')
    
    def get_connection(self):
        """获取数据库连接"""
        if self.is_postgres and POSTGRES_AVAILABLE:
            return psycopg2.connect(Config.get_db_connection_string())
        else:
            # 使用 SQLite
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
    
    def init_db(self):
        """初始化数据库表"""
        if self.is_postgres and POSTGRES_AVAILABLE:
            self._init_postgres()
        else:
            self._init_sqlite()
    
    def _init_sqlite(self):
        """初始化 SQLite 数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 策略表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS strategies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_code TEXT UNIQUE NOT NULL,
                strategy_name TEXT NOT NULL,
                strategy_type TEXT NOT NULL,
                business_type TEXT NOT NULL,
                futures_contract TEXT,
                futures_contract2 TEXT,
                spot_variety TEXT,
                forward_variety TEXT,
                futures_direction TEXT,
                spot_direction TEXT,
                plan_quantity REAL,
                apply_org TEXT,
                apply_person TEXT,
                apply_date TEXT,
                valid_until TEXT,
                current_basis REAL,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 策略分析表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS strategy_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_id INTEGER NOT NULL,
                operation_scale TEXT,
                operation_direction TEXT,
                core_logic TEXT,
                execution_plan TEXT,
                risk_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (strategy_id) REFERENCES strategies(id) ON DELETE CASCADE
            )
        ''')
        
        # 数据文件记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_type TEXT NOT NULL,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_data BLOB,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 主力合约配置表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS main_contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                variety TEXT NOT NULL,
                contract_code TEXT NOT NULL,
                effective_date TEXT NOT NULL,
                expiry_date TEXT NOT NULL
            )
        ''')
        
        # 周报内容表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_week TEXT NOT NULL,
                market_review TEXT,
                production_status TEXT,
                demand_status TEXT,
                inventory_status TEXT,
                macro_outlook TEXT,
                cost_outlook TEXT,
                technical_outlook TEXT,
                market_view TEXT,
                rb_key_levels TEXT,
                hc_key_levels TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("SQLite 数据库初始化完成")
    
    def _init_postgres(self):
        """初始化 PostgreSQL 数据库"""
        conn = psycopg2.connect(Config.get_db_connection_string())
        cursor = conn.cursor()
        
        # 策略表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS strategies (
                id SERIAL PRIMARY KEY,
                strategy_code VARCHAR(50) UNIQUE NOT NULL,
                strategy_name VARCHAR(200) NOT NULL,
                strategy_type VARCHAR(50) NOT NULL,
                business_type VARCHAR(50) NOT NULL,
                futures_contract VARCHAR(50),
                futures_contract2 VARCHAR(50),
                spot_variety VARCHAR(100),
                forward_variety VARCHAR(100),
                futures_direction VARCHAR(10),
                spot_direction VARCHAR(10),
                plan_quantity NUMERIC,
                apply_org VARCHAR(200),
                apply_person VARCHAR(100),
                apply_date DATE,
                valid_until DATE,
                current_basis NUMERIC,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 策略分析表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS strategy_analysis (
                id SERIAL PRIMARY KEY,
                strategy_id INTEGER NOT NULL REFERENCES strategies(id) ON DELETE CASCADE,
                operation_scale TEXT,
                operation_direction TEXT,
                core_logic TEXT,
                execution_plan TEXT,
                risk_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 数据文件记录表 - 云端存储文件数据
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_files (
                id SERIAL PRIMARY KEY,
                file_type VARCHAR(50) NOT NULL,
                file_name VARCHAR(500) NOT NULL,
                file_path TEXT NOT NULL,
                file_data BYTEA,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 主力合约配置表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS main_contracts (
                id SERIAL PRIMARY KEY,
                variety VARCHAR(50) NOT NULL,
                contract_code VARCHAR(50) NOT NULL,
                effective_date DATE NOT NULL,
                expiry_date DATE NOT NULL
            )
        ''')
        
        # 周报内容表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_reports (
                id SERIAL PRIMARY KEY,
                report_week VARCHAR(50) NOT NULL,
                market_review TEXT,
                production_status TEXT,
                demand_status TEXT,
                inventory_status TEXT,
                macro_outlook TEXT,
                cost_outlook TEXT,
                technical_outlook TEXT,
                market_view TEXT,
                rb_key_levels TEXT,
                hc_key_levels TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("PostgreSQL 数据库初始化完成")

# 全局实例
db_manager = DatabaseManager()

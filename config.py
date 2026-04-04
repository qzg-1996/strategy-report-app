"""
配置文件 - 支持本地和云端环境
"""
import os

# 环境变量配置
class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    
    # 数据库配置 - 优先使用环境变量（云端），否则使用本地 SQLite
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///strategy.db')
    
    # Supabase 配置
    SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')
    
    # 上传文件夹
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    @staticmethod
    def is_production():
        """判断是否生产环境（云端）"""
        return os.environ.get('RENDER', '') != '' or os.environ.get('DATABASE_URL', '').startswith('postgresql')
    
    @staticmethod
    def get_db_connection_string():
        """获取数据库连接字符串"""
        db_url = Config.DATABASE_URL
        # Render 等平台使用 postgres://，SQLAlchemy 需要 postgresql://
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        return db_url

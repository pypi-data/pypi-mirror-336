# redshift_connector_bade/__init__.py

"""
redshift_connector_bade
一個簡單的 Amazon Redshift JDBC 查詢工具
"""

from .connector import fetch_data_from_redshift

__all__ = ["fetch_data_from_redshift"]

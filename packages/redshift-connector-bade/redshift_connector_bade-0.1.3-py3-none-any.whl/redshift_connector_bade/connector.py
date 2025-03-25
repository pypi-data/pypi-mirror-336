#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import jpype
import jaydebeapi
import pandas as pd

def fetch_data_from_redshift(jvm_path, jdbc_driver_path, aws_sdk_path, jdbc_url, query):
    """
    從 Redshift 資料庫中執行查詢並返回結果。
    
    jvm_path: JVM 路徑
    jdbc_driver_path: Redshift JDBC 驅動路徑
    aws_sdk_path: AWS SDK 路徑
    jdbc_url: JDBC 連線 URL
    query: 要執行的 SQL 查詢語句
    """
    # 啟動 JVM，確保類路徑包含 JDBC 驅動和 AWS SDK
    if not jpype.isJVMStarted():
        jpype.startJVM(jvm_path, f"-Djava.class.path={jdbc_driver_path};{aws_sdk_path}")

    # 選擇正確的 Driver
    driver_class = "com.amazon.redshift.jdbc42.Driver"

    # 連接到 Redshift 資料庫
    conn = jaydebeapi.connect(
        driver_class,
        jdbc_url,
        [],  # 不需要傳遞其他參數
        [jdbc_driver_path, aws_sdk_path]  # 同時加載 Redshift JDBC 和 AWS SDK
    )

    # 執行 SQL 查詢
    cursor = conn.cursor()
    cursor.execute(query)

    # 獲取查詢結果
    rows = cursor.fetchall()

    # 獲取列名並去除空格
    columns = [str(desc[0]).strip() for desc in cursor.description]

    # 將查詢結果轉換為 DataFrame
    df = pd.DataFrame(rows, columns=columns)

    # 處理每列中的資料，將元組拼接為字串
    for column in df.columns:
        df[column] = df[column].apply(lambda x: ''.join([str(i).strip() for i in x]) if isinstance(x, (tuple, list)) else str(x).strip())

    # 關閉連接
    conn.close()

    return df


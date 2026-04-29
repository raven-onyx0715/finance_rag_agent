import fitz
import os

# 创建测试PDF内容
content = """
财务报告

2025年财务摘要

营业收入：1000万元
净利润：200万元
资产负债率：40%

详细财务数据

第一季度：
营业收入：200万元
净利润：40万元

第二季度：
营业收入：250万元
净利润：50万元

第三季度：
营业收入：280万元
净利润：56万元

第四季度：
营业收入：270万元
净利润：54万元

财务分析

公司2025年营业收入同比增长10%，净利润同比增长15%，资产负债率保持在合理水平。
"""

# 生成PDF文件
doc = fitz.open()
page = doc.new_page()
page.insert_text((50, 50), content)

# 保存到桌面的financial_rag/data目录
output_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'financial_rag', 'data', 'test_report.pdf')
doc.save(output_path)
doc.close()

print(f"测试PDF文件已生成：{output_path}")

# frozen_string_literal: true

# 检查文件是否存在
# 参数:
#   file_path 文件路径
# 返回值:
#   是否存在
def file_exist?(file_path)
  File.exist?(file_path)
end


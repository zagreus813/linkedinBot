import pandas as pd
import os

class ExcelService:
    def __init__(self, file_path):
        self.file_path = file_path
        # چک کنیم فایل وجود دارد یا نه
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel file not found at: {file_path}")

    def get_pending_post(self):
        """اولین پست با وضعیت Pending را برمی‌گرداند"""
        try:
            # خواندن فایل اکسل
            df = pd.read_excel(self.file_path)
            
            # نرمال کردن نام ستون‌ها (حذف فاصله‌های احتمالی)
            df.columns = [c.strip() for c in df.columns]
            
            # فیلتر کردن
            pending_mask = df['Status'].str.lower() == 'pending'
            pending_rows = df[pending_mask]
            
            if not pending_rows.empty:
                # اولین ردیف پیدا شده
                first_index = pending_rows.index[0]
                return {
                    "index": first_index, # شماره ایندکس در دیتافریم
                    "content": pending_rows.iloc[0]['Content']
                }
            return None
        except Exception as e:
            print(f"Error reading Excel: {e}")
            return None

    def mark_as_published(self, index):
        """وضعیت را در فایل اکسل ذخیره می‌کند"""
        try:
            df = pd.read_excel(self.file_path)
            
            # تغییر وضعیت
            df.at[index, 'Status'] = 'Published'
            
            # ذخیره مجدد در فایل (بدون ایندکس اضافی)
            df.to_excel(self.file_path, index=False)
            return True, "Excel updated successfully."
        except PermissionError:
            return False, "Error: Close the Excel file! It is open by another program."
        except Exception as e:
            return False, f"Error updating Excel: {e}"
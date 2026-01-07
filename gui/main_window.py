import customtkinter as ctk
import threading
import schedule
import time
from datetime import datetime
import os
from tkinter import filedialog 
from core.excel_service import ExcelService 
from core.linkedin_service import LinkedInService
from dotenv import load_dotenv

# تنظیم تم پیشرفته
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        load_dotenv()

        # تنظیمات پنجره
        self.title("🤖 LinkedIn Pro Agent v2.0")
        self.geometry("850x600")
        self.resizable(True, True)
        self.minsize(800, 550)

        # تنظیمات فونت
        self.title_font = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.subtitle_font = ctk.CTkFont(family="Segoe UI", size=14)
        self.log_font = ctk.CTkFont(family="Consolas", size=12)
        self.button_font = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")

        # رنگ‌های سفارشی
        self.primary_color = "#2B7CD3"
        self.success_color = "#10B981"
        self.error_color = "#EF4444"
        self.warning_color = "#F59E0B"
        self.sidebar_color = "#1E293B"

        # گرید بندی
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # سایدبار مدرن
        self.sidebar_frame = ctk.CTkFrame(
            self, 
            width=220, 
            corner_radius=0,
            fg_color=self.sidebar_color
        )
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=(0, 2))
        self.sidebar_frame.grid_propagate(False)

        # لوگو و عنوان سایدبار
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="🤖\nAutoPoster Pro",
            font=self.title_font,
            justify="center"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))
        # دکمه انتخاب فایل اکسل (جدید)
        self.file_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="📂 Select Excel File",
            font=self.button_font,
            fg_color="#4F46E5", # رنگ بنفش برای تمایز
            hover_color="#4338CA",
            height=45,
            corner_radius=10,
            command=self.select_file # تابعی که پایین‌تر می‌سازیم
        )
        self.file_btn.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")
        
        # لیبل نمایش نام فایل
        self.file_label = ctk.CTkLabel(self.sidebar_frame, text="No file selected", font=ctk.CTkFont(size=11), text_color="gray")
        self.file_label.grid(row=2, column=0, padx=20, pady=(0, 10))

        # (نکته: عدد row دکمه‌های start و stop را باید یکی زیاد کنید تا پایین‌تر بروند)   
        # آیکون‌های Material Design (با استفاده از emoji)
        self.start_button = ctk.CTkButton(
            self.sidebar_frame,
            text="▶️ START AGENT",
            font=self.button_font,
            fg_color=self.success_color,
            hover_color="#059669",
            height=45,
            corner_radius=10,
            command=self.start_agent
        )
        self.start_button.grid(row=5, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.stop_button = ctk.CTkButton(
            self.sidebar_frame,
            text="⏹️ STOP AGENT",
            font=self.button_font,
            fg_color=self.error_color,
            hover_color="#DC2626",
            height=45,
            corner_radius=10,
            state="disabled",
            command=self.stop_agent
        )
        self.stop_button.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        # بخش اطلاعات
        self.info_frame = ctk.CTkFrame(
            self.sidebar_frame,
            fg_color="transparent",
            border_width=0
        )
        self.info_frame.grid(row=3, column=0, padx=20, pady=(30, 20), sticky="s")

        self.schedule_label = ctk.CTkLabel(
            self.info_frame,
            text="📅 Schedule:\n• Sunday 10:00 AM\n• Tuesday 10:00 AM",
            font=self.subtitle_font,
            justify="left"
        )
        self.schedule_label.pack(pady=(0, 20))

        # وضعیت
        self.status_indicator = ctk.CTkLabel(
            self.info_frame,
            text="●",
            font=ctk.CTkFont(size=24),
            text_color="gray"
        )
        self.status_indicator.pack(pady=(0, 5))

        self.status_text = ctk.CTkLabel(
            self.info_frame,
            text="IDLE",
            font=self.subtitle_font
        )
        self.status_text.pack()

        # بخش اصلی
        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            border_width=2,
            border_color="#374151"
        )
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # هدر بخش اصلی
        self.header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
            height=60
        )
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.main_title = ctk.CTkLabel(
            self.header_frame,
            text="Activity Logs & Monitoring",
            font=self.title_font
        )
        self.main_title.grid(row=0, column=0, sticky="w")

        self.stats_frame = ctk.CTkFrame(
            self.header_frame,
            fg_color="#1F2937",
            corner_radius=10,
            height=40
        )
        self.stats_frame.grid(row=0, column=1, sticky="e")

        self.next_run_label = ctk.CTkLabel(
            self.stats_frame,
            text="Next Run: --:--",
            font=self.subtitle_font,
            padx=10
        )
        self.next_run_label.pack(side="left", padx=10, pady=5)

        # ناحیه لاگ‌ها با ظاهری مدرن
        self.log_container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=10
        )
        self.log_container.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.log_container.grid_columnconfigure(0, weight=1)
        self.log_container.grid_rowconfigure(0, weight=1)

        # هدر لاگ
        self.log_header = ctk.CTkFrame(
            self.log_container,
            fg_color="#1F2937",
            height=40,
            corner_radius=10
        )
        self.log_header.grid(row=0, column=0, sticky="ew", padx=1, pady=(1, 0))
        
        self.log_title = ctk.CTkLabel(
            self.log_header,
            text="System Logs",
            font=self.button_font
        )
        self.log_title.pack(side="left", padx=15)

        self.clear_logs_btn = ctk.CTkButton(
            self.log_header,
            text="Clear Logs",
            width=80,
            height=30,
            font=self.subtitle_font,
            command=self.clear_logs
        )
        self.clear_logs_btn.pack(side="right", padx=10, pady=5)

        # جعبه متن لاگ‌ها
        self.log_textbox = ctk.CTkTextbox(
            self.log_container,
            font=self.log_font,
            corner_radius=10,
            border_width=0
        )
        self.log_textbox.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
        self.log_textbox.configure(fg_color="#0F172A")

        # نوار وضعیت پایین
        self.footer_frame = ctk.CTkFrame(
            self.main_frame,
            height=40,
            corner_radius=10,
            fg_color="#1F2937"
        )
        self.footer_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.last_update_label = ctk.CTkLabel(
            self.footer_frame,
            text="Last Update: --:--:--",
            font=self.subtitle_font
        )
        self.last_update_label.pack(side="left", padx=15)

        self.log_count_label = ctk.CTkLabel(
            self.footer_frame,
            text="Logs: 0",
            font=self.subtitle_font
        )
        self.log_count_label.pack(side="right", padx=15)

        # متغیرهای کنترلی
        self.running = False
        self.scheduler_thread = None
        self.log_count = 0
        self.excel_path = None
        # پیام خوش‌آمدگویی
        self.log("🚀 LinkedIn Pro Agent v2.0 Initialized")
        self.log("📋 Loaded environment variables")
        self.log("⏳ Ready to start - Press START AGENT")
        self.update_log_count()
    def select_file(self):
        """انتخاب فایل اکسل"""
        filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if filename:
            self.excel_path = filename
            short_name = os.path.basename(filename)
            self.file_label.configure(text=f"📄 {short_name}", text_color=self.success_color)
            self.log(f"📂 Excel file selected: {short_name}")
    def clear_logs(self):
        """پاک کردن لاگ‌ها"""
        self.log_textbox.delete("1.0", "end")
        self.log_count = 0
        self.update_log_count()
        self.log("🧹 Logs cleared")

    def update_log_count(self):
        """به‌روزرسانی تعداد لاگ‌ها"""
        self.log_count_label.configure(text=f"Logs: {self.log_count}")

    def log(self, message):
        """ثبت لاگ با فرمت‌بندی رنگی"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # تشخیص نوع پیام و رنگ مناسب
        if "✅" in message or "SUCCESS" in message.upper():
            color_tag = "success"
        elif "❌" in message or "ERROR" in message.upper():
            color_tag = "error"
        elif "⚠️" in message or "WARNING" in message.upper():
            color_tag = "warning"
        else:
            color_tag = "info"
        
        # تنظیم تگ‌های رنگی
        colors = {
            "success": self.success_color,
            "error": self.error_color,
            "warning": self.warning_color,
            "info": "#6B7280"
        }
        
        # درج لاگ با رنگ
        self.log_textbox.insert("end", f"[{timestamp}] ", "timestamp")
        self.log_textbox.insert("end", f"{message}\n", color_tag)
        
        # تنظیم تگ‌ها
        self.log_textbox.tag_config("timestamp", foreground="#9CA3AF")
        self.log_textbox.tag_config("success", foreground=self.success_color)
        self.log_textbox.tag_config("error", foreground=self.error_color)
        self.log_textbox.tag_config("warning", foreground=self.warning_color)
        self.log_textbox.tag_config("info", foreground="#D1D5DB")
        
        self.log_textbox.see("end")
        self.log_count += 1
        self.update_log_count()
        self.last_update_label.configure(text=f"Last Update: {datetime.now().strftime('%H:%M:%S')}")

    # def job(self):
    #     """وظیفه اصلی برنامه"""
    #     self.log("🔍 Checking for pending posts...")
    #     try:
    #         # اتصال به سرویس‌ها
    #         self.log("📡 Connecting to Google Sheets...")
    #         gs = GoogleService(os.getenv("GOOGLE_CREDENTIALS_FILE"), os.getenv("GOOGLE_SHEET_URL"))
            
    #         self.log("📡 Connecting to LinkedIn API...")
    #         li = LinkedInService(os.getenv("LINKEDIN_ACCESS_TOKEN"))
            
    #         pending_posts = gs.get_pending_posts()
            
    #         if not pending_posts:
    #             self.log("📭 No pending posts found.")
    #             return

    #         # گرفتن اولین پست
    #         post_to_publish = pending_posts[0]
    #         self.log(f"📤 Publishing post: {post_to_publish['content'][:50]}...")
            
    #         # ارسال به لینکدین
    #         success, msg = li.post_text(post_to_publish['content'])
            
    #         if success:
    #             gs.mark_as_published(post_to_publish['row'])
    #             self.log(f"✅ Published successfully! Post ID: {msg}")
    #         else:
    #             self.log(f"❌ Error publishing: {msg}")

    #     except Exception as e:
    #         self.log(f"❌ Critical Error: {str(e)}")
    def job(self):
        """وظیفه اصلی برنامه (نسخه اکسل)"""
        self.log("🔍 Checking schedule & file...")
        try:
            # 1. چک کردن فایل اکسل
            if not self.excel_path:
                self.log("❌ Error: No Excel file selected!")
                return

            # 2. اتصال به سرویس‌ها
            self.log("📖 Reading Excel file...")
            excel_service = ExcelService(self.excel_path)
            
            self.log("📡 Connecting to LinkedIn API...")
            li = LinkedInService(os.getenv("LINKEDIN_ACCESS_TOKEN"))
            
            # 3. دریافت پست
            post_data = excel_service.get_pending_post()
            
            if not post_data:
                self.log("📭 No 'Pending' posts found in Excel.")
                return

            # استخراج داده‌ها
            content = post_data['content']
            index = post_data['index']

            self.log(f"📤 Publishing: {str(content)[:40]}...")
            
            # 4. ارسال به لینکدین
            success, msg = li.post_text(str(content))
            
            if success:
                # 5. آپدیت اکسل
                ok, update_msg = excel_service.mark_as_published(index)
                if ok:
                    self.log(f"✅ Published & Excel Updated! ID: {msg}")
                else:
                    self.log(f"⚠️ Published but Excel Error: {update_msg}")
            else:
                self.log(f"❌ LinkedIn Error: {msg}")

        except Exception as e:
            self.log(f"❌ Critical Error: {str(e)}")
    def run_scheduler(self):
        """اجرای زمان‌بند"""
        # زمان‌بندی اصلی
        schedule.every().sunday.at("10:00").do(self.job)
        schedule.every().tuesday.at("10:00").do(self.job)
        
        # برای تست (هر 2 دقیقه) - بعداً غیرفعال کنید
        schedule.every(2).minutes.do(self.job)

        while self.running:
            schedule.run_pending()
            
            # به‌روزرسانی زمان اجرای بعدی
            next_run = schedule.next_run()
            if next_run:
                next_run_str = next_run.strftime("%Y-%m-%d %H:%M")
                self.next_run_label.configure(text=f"Next Run: {next_run_str}")
            
            time.sleep(1)

    def start_agent(self):
        """شروع عامل"""
        if not self.excel_path:
            self.log("⚠️ Please select an Excel file first!")
            return
        if not self.running:
            self.running = True
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            
            # به‌روزرسانی وضعیت
            self.status_indicator.configure(text_color=self.success_color)
            self.status_text.configure(text="RUNNING", text_color=self.success_color)
            
            self.log("🚀 Agent Started Successfully")
            self.log("⏰ Scheduled Jobs: Sunday & Tuesday at 10:00 AM")
            self.log("📊 Monitoring for pending posts...")
            
            # شروع thread زمان‌بند
            self.scheduler_thread = threading.Thread(target=self.run_scheduler)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()

    def stop_agent(self):
        """توقف عامل"""
        self.running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
        # به‌روزرسانی وضعیت
        self.status_indicator.configure(text_color="gray")
        self.status_text.configure(text="STOPPED", text_color="gray")
        self.next_run_label.configure(text="Next Run: --:--")
        
        self.log("🛑 Agent Stopped")
        self.log("📊 All scheduled jobs cleared")

if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()
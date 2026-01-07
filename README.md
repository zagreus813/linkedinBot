# LinkedIn AutoPoster Pro 🤖

**LinkedIn AutoPoster Pro** is a modern, Python-based desktop application designed to automate content publishing on LinkedIn. Built with a sleek **CustomTkinter** GUI, it allows users to schedule posts from a local **Excel** file without relying on complex cloud databases.

The agent runs locally, reads content from an Excel sheet, posts to your LinkedIn profile via API, and automatically updates the status of each post to prevent duplicates.

<img width="852" height="632" alt="image" src="https://github.com/user-attachments/assets/043dad24-4095-4823-afbb-515b6575fa0d" />

---

## ✨ Features

- **🎨 Modern Dark UI:** Built with `CustomTkinter` for a professional, responsive user experience.
- **📂 Local Data Management:** Uses a simple Excel file (`.xlsx`) to manage content and tracking.
- **⏱️ Automated Scheduling:** Pre-configured to post automatically on **Sundays** and **Tuesdays** at 10:00 AM (customizable).
- **📝 Status Tracking:** Automatically marks posts as `Published` in the Excel file after successful submission.
- **🔒 Secure:** Sensitive data (API Tokens) are stored in a local `.env` file.
- **📦 Standalone Executable:** Can be compiled into a single `.exe` file for ease of use.

---

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **GUI:** CustomTkinter
- **Data:** Pandas, OpenPyXL (Excel)
- **Scheduling:** Schedule Library
- **API:** LinkedIn REST API
- **Build Tool:** PyInstaller

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/LinkedIn-AutoPoster.git](https://github.com/YOUR_USERNAME/LinkedIn-AutoPoster.git)
cd LinkedIn-AutoPoster

```

### 2. Install Dependencies

It is recommended to use a virtual environment.

```bash
pip install -r requirements.txt

```

*(Note: If you don't have a `requirements.txt`, install manually: `pip install customtkinter pandas openpyxl schedule python-dotenv requests pyinstaller`)*

### 3. Configuration (.env)

Create a file named `.env` in the root directory and add your LinkedIn Access Token:

```env
LINKEDIN_ACCESS_TOKEN=your_long_access_token_here

```

> **Note:** LinkedIn Access Tokens typically expire after **60 days**. You will need to generate a new one and update this file periodically.

---

## 📊 Excel File Structure

Create an Excel file (e.g., `posts.xlsx`) with the following headers in the first row:

| Content | Status |
| --- | --- |
| This is my first post about AI... | Pending |
| Checking out this new automation tool! | Pending |
| Another great post... | Published |

* **Content:** The text you want to post.
* **Status:** Must be `Pending` for the agent to pick it up. The agent will change this to `Published` automatically.

---

## 🔑 How to Get LinkedIn Access Token

1. Go to [LinkedIn Developers Portal](https://www.linkedin.com/developers/apps).
2. Create a new App (you need a Company Page associated with it).
3. In the **Products** tab, request access to **"Share on LinkedIn"** and **"Sign In with LinkedIn"**.
4. Go to **Auth** > **OAuth 2.0 Tools**.
5. Create a token with the following scopes: `openid`, `profile`, `email`, `w_member_social`.
6. Copy the generated Access Token into your `.env` file.

---

## 🏗️ Build Standalone (.exe)

To convert the Python script into a Windows executable file, run the following command in your terminal:

```bash
pyinstaller --noconfirm --onefile --windowed --name "LinkedInPoster" --add-data "core;core" main.py

```

After the build completes:

1. Go to the `dist` folder.
2. Move `LinkedInPoster.exe` to a new folder.
3. **Crucial:** Copy your `.env` file and your `posts.xlsx` file next to the `.exe`.

---

## 📂 Project Structure

```text
LinkedIn-AutoPoster/
│
├── core/
│   ├── excel_service.py    # Handles Excel reading/writing
│   └── linkedin_service.py # Handles LinkedIn API requests
│
├── gui/
│   └── main_window.py      # CustomTkinter GUI Logic
│
├── assets/                 # Icons and images
├── .env                    # API Keys (Not uploaded to GitHub)
├── main.py                 # Entry point
├── README.md               # Documentation
└── requirements.txt        # Dependencies

```

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and create a pull request for any features or bug fixes.

## 📄 License

This project is licensed under the MIT License.

```

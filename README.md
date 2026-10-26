# OOP2-FINAL-PROJECT-GROUP3


![image alt](https://github.com/RebagosBSCpE/OOP2-FINAL-PROJECT-GROUP3/blob/main/Laboratory%20Equipment%20Borrowing%20and%20Inventory%20Management%20System.png?raw=true)


<br>

## 📌 About the Project

In most school laboratories, borrowing equipment relies on a paper-based method students fill out physical slips, hunt down professors for signatures, and hand them to the laboratory staff to write down. Paper forms get lost, signatures are hard to track down, and staff cannot easily verify which items are currently available or who holds what.

This PyQt6 desktop application eliminates paper-based methods to make borrowing faster, more convenient, and easily accessible at any time. It keeps the same borrowing steps but digitizes them in one centralized system students submit borrowing requests digitally, professors approve or reject them online, and laboratory staff release and receive items while maintaining staff-based records and real-time inventory updates. Packaged as a standalone .exe, this PyQt6 application solves the problem by preventing lost slips, stopping invalid requests, and keeping stock counts automatically accurate.

<br>

## 👥 Who Uses It

<table>
<tr>
<td width="33%" valign="top">

### 🎓 Student
- Logs in and fills out a borrow slip
- Picks items, quantities, purpose, and date needed
- Chooses which professor receives the slip
- Tracks the slip status

</td>
<td width="33%" valign="top">

### 👨‍🏫 Professor
- Logs in and sees slips sent to him or her
- Approves or rejects each slip
- Adds optional remarks

</td>
<td width="33%" valign="top">

### 🧑‍🔧 Laboratory Staff
- Logs in and sees approved slips
- Releases items against the student ID
- Receives returned items
- See the available materials inside inventory

</td>
</tr>
</table>


## ✨ Features

| | Feature | Description |
|:-:|---|---|
| 🔐 | **Role-based login** | Opens the dashboard that matches the user: student, professor, or staff |
| 📝 | **Borrow slip form** | Items, quantities, purpose, date needed, and the professor to send it to |
| 📊 | **Slip tracking** | Statuses: Pending, Approved, Rejected, Released, Returned |
| ✅ | **Approve or reject** | Professors review their slips with optional remarks |
| 📦 | **Release and return** | Staff verify the student ID, release items, and receive returns |
| 🗃️ | **Inventory management** | Add, edit, and delete equipment with total, available, and borrowed counts |
| 💾 | **Save and load** | Users, equipment, and slips are stored in `csv` and kept after closing |
| 🧭 | **Menu bar and toolbar** | Save, Logout, and Exit|
| 🛡️ | **Input validation** | Blocks empty fields, zero or excessive quantities, and unavailable items |

<br>

## 🧰 Tech Stack

| Tool | Purpose |
|---|---|
| **Python** | Programming language |
| **PyQt6** | Graphical user interface |
| **QSS (Qt Style Sheets)** | White, yellow, and black theme |
| **csv** | Saving and loading data |
| **PyInstaller** | Packaging as a Windows `.exe` |
| **Git and GitHub** | Version control and teamwork |



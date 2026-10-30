<div align="center">

# OOP2-FINAL-PROJECT-GROUP3

<img src="https://placehold.co/900x10/FADE00/FADE00" width="100%" alt="">
<img src="https://placehold.co/900x10/231F20/231F20" width="100%" alt="">

![image alt](https://github.com/RebagosBSCpE/OOP2-FINAL-PROJECT-GROUP3/blob/main/Laboratory%20Equipment%20Borrowing%20and%20Inventory%20Management%20System.png?raw=true)

<img src="https://img.shields.io/badge/Python-3.12-FADE00?style=for-the-badge&labelColor=231F20" alt="Python 3.12">
<img src="https://img.shields.io/badge/PyQt6-6.11.0-FADE00?style=for-the-badge&labelColor=231F20" alt="PyQt6 6.11.0">
<img src="https://img.shields.io/badge/Storage-CSV-FADE00?style=for-the-badge&labelColor=231F20" alt="Storage CSV">
<img src="https://img.shields.io/badge/Packaged%20with-PyInstaller-FADE00?style=for-the-badge&labelColor=231F20" alt="PyInstaller">
<img src="https://img.shields.io/badge/CPE%20009B-OOP%202-BCBDC1?style=for-the-badge&labelColor=231F20" alt="CPE 009B OOP 2">

<img src="https://placehold.co/900x10/231F20/231F20" width="100%" alt="">
<img src="https://placehold.co/900x10/FADE00/FADE00" width="100%" alt="">

</div>

<br>

<img src="https://img.shields.io/badge/ABOUT-THE%20PROJECT-FADE00?style=for-the-badge&labelColor=231F20" alt="About the Project">

In most school laboratories, borrowing equipment relies on a paper-based method students fill out physical slips, hunt down professors for signatures, and hand them to the laboratory staff to write down. Paper forms get lost, signatures are hard to track down, and staff cannot easily verify which items are currently available or who holds what.

This PyQt6 desktop application eliminates paper-based methods to make borrowing faster, more convenient, and easily accessible at any time. It keeps the same borrowing steps but digitizes them in one centralized system students submit borrowing requests digitally, every request is recorded in the ITSO CSV log, professors approve or reject them online, and laboratory staff release and receive items while maintaining staff-based records and real-time inventory updates. Packaged as a standalone .exe, this PyQt6 application solves the problem by preventing lost slips, stopping invalid requests, and keeping stock counts automatically accurate.

<img src="https://placehold.co/900x4/BCBDC1/BCBDC1" width="100%" alt="">

<br>

<img src="https://img.shields.io/badge/WHO-USES%20IT-FADE00?style=for-the-badge&labelColor=231F20" alt="Who Uses It">

<table>
<tr>
<td width="25%" valign="top">

<img src="https://img.shields.io/badge/-STUDENT-231F20?style=flat-square" alt="Student">

- Logs in and fills out a borrow slip
- Picks items, quantities, purpose, and date needed
- Chooses which professor receives the slip
- Tracks the slip status

</td>
<td width="25%" valign="top">

<img src="https://img.shields.io/badge/-ITSO-FADE00?style=flat-square&labelColor=FADE00" alt="ITSO">

- Logs in and sees every submitted request in the CSV log
- Refreshes the log to see the newest requests and statuses
- Generates or deletes a backup folder of the records

</td>
<td width="25%" valign="top">

<img src="https://img.shields.io/badge/-PROFESSOR-231F20?style=flat-square" alt="Professor">

- Logs in and sees slips sent to him or her
- Approves or rejects each slip
- Adds optional remarks

</td>
<td width="25%" valign="top">

<img src="https://img.shields.io/badge/-LAB%20STAFF-FADE00?style=flat-square&labelColor=FADE00" alt="Laboratory Staff">

- Logs in and sees approved slips
- Releases items against the student ID
- Receives returned items
- See the available materials inside inventory

</td>
</tr>
</table>

<img src="https://placehold.co/900x4/BCBDC1/BCBDC1" width="100%" alt="">

<br>

<img src="https://img.shields.io/badge/KEY-FEATURES-FADE00?style=for-the-badge&labelColor=231F20" alt="Features">

| | Feature | Description |
|:-:|---|---|
| <img src="https://img.shields.io/badge/01-FADE00?style=flat-square" alt="01"> | **Role-based login** | Opens the dashboard that matches the user: student, ITSO, professor, or staff |
| <img src="https://img.shields.io/badge/02-FADE00?style=flat-square" alt="02"> | **Borrow slip form** | Items, quantities, purpose, date needed, and the professor to send it to |
| <img src="https://img.shields.io/badge/03-FADE00?style=flat-square" alt="03"> | **ITSO maintenance dashboard** | Shows every submitted request in a table, with Sync / Refresh CSV Log, Generate Backup Folder, and Delete Backup Folder |
| <img src="https://img.shields.io/badge/04-FADE00?style=flat-square" alt="04"> | **CSV request log** | Each submitted slip is saved automatically in the ITSO CSV log, and every status change is updated in it |
| <img src="https://img.shields.io/badge/05-FADE00?style=flat-square" alt="05"> | **Slip tracking** | Statuses: Pending, Approved, Rejected, Released, Returned |
| <img src="https://img.shields.io/badge/06-FADE00?style=flat-square" alt="06"> | **Approve or reject** | Professors review their slips with optional remarks |
| <img src="https://img.shields.io/badge/07-FADE00?style=flat-square" alt="07"> | **Release and return** | Staff verify the student ID, release items, and receive returns |
| <img src="https://img.shields.io/badge/08-FADE00?style=flat-square" alt="08"> | **Inventory management** | Add, edit, and delete equipment with total, available, and borrowed counts |
| <img src="https://img.shields.io/badge/09-FADE00?style=flat-square" alt="09"> | **Save and load** | Users, equipment, and slips are stored in `csv` and kept after closing |
| <img src="https://img.shields.io/badge/10-FADE00?style=flat-square" alt="10"> | **Menu bar and toolbar** | Save, Logout, and Exit|
| <img src="https://img.shields.io/badge/11-FADE00?style=flat-square" alt="11"> | **Input validation** | Blocks empty fields, zero or excessive quantities, and unavailable items |

<img src="https://placehold.co/900x4/BCBDC1/BCBDC1" width="100%" alt="">

<br>

<img src="https://img.shields.io/badge/TECH-STACK-FADE00?style=for-the-badge&labelColor=231F20" alt="Tech Stack">

| Tool | Purpose |
|---|---|
| **Python** | Programming language |
| **PyQt6** | Graphical user interface |
| **QSS (Qt Style Sheets)** | White, yellow, and black theme |
| **Csv** | Saving and loading data |
| **PyInstaller** | Packaging as a Windows .exe |
| **Git and GitHub** | Version control and teamwork |

<br>

<div align="center">

<img src="https://placehold.co/900x10/FADE00/FADE00" width="100%" alt="">
<img src="https://placehold.co/900x10/231F20/231F20" width="100%" alt="">

<img src="https://img.shields.io/badge/TECHNOLOGICAL%20INSTITUTE-OF%20THE%20PHILIPPINES-FADE00?style=for-the-badge&labelColor=231F20" alt="Technological Institute of the Philippines">

</div>

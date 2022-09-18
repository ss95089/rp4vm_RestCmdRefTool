# rp4vm_RestCmdRefTool

This tool replaces and displays RecoverPoint for VMs operations in Curl commands (REST API).  
I created this tool as a confirmation tool for job control of RecoverPoint for VMs from job management software.  
The supported operations are as follows
 - ProtectVM
 - Add MV to existing Consistency Group
 - Create Bookmark
 - Test a Copy
 - Failover / Recover Production
 - Rmove CG

*Group sets and multi-site copying are not supported.

---
### image
![image](https://user-images.githubusercontent.com/67679613/190887144-7fd0f7a8-95d1-41de-94c6-4a5cfbe7324c.gif)

---
### download
You can download the converted file to exe in pyinstaller for Windows 10 (64bit).  
After unzipping, run rp4vm_RestCmdRefTool_v0.XX.exe.  


[rp4vm_RestCmdRefTool_v0.90.zip](https://github.com/ss95089/rp4vm_RestCmdRefTool/raw/main/dist/rp4vm_RestCmdRefTool_v0.90.zip)  
---
### development environment
RecoverPoint for Virtual Machines 5.3 SP2 P4  
Python 3.8.9  


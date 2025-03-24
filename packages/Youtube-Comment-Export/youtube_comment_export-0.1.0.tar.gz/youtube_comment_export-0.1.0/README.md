<h1 align="center">Youtube Comment Export</h1>

<h3 align="center">Export the comments of a YouTube channel in Excel files.</h3>

<div align="center">
    
  [![PyPI](https://img.shields.io/pypi/v/Youtube-Comment-Export?style=flat)](https://pypi.org/project/Youtube-Comment-Export)
  <a href="https://opensource.org/license/mit">![License](https://img.shields.io/badge/License-MIT-blue)</a>
  <a href="https://github.com/Atem83/Youtube-Comment-Export/archive/refs/heads/main.zip">![Download](https://img.shields.io/badge/Source_Code-Download-blue)</a>
  ![LOC](https://tokei.rs/b1/github/Atem83/Youtube-Comment-Export?category=lines)
  
</div>

<div align="center">
  <div style="display: flex; justify-content: space-around;">
    <img src="https://raw.githubusercontent.com/Atem83/Youtube-Comment-Export/main/images/GUI light theme.png" alt="GUI Light Theme" style="width: 35%;">
    <img src="https://raw.githubusercontent.com/Atem83/Youtube-Comment-Export/main/images/GUI dark theme.png" alt="GUI Dark Theme" style="width: 35%;">
  </div>
</div>

<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/Atem83/Youtube-Comment-Export/main/images/GUI Settings.png" alt="GUI Settings" style="width: 35%;">
</div>

<h2 align="center"> Excel Main Sheet </h2>

<div align="center">
  <img src="https://raw.githubusercontent.com/Atem83/Youtube-Comment-Export/main/images/Excel videos sheet.png" alt="Excel videos sheet" style="width: 100%;">
</div>

<h2 align="center"> Excel Comments Sheet </h2>

<div align="center">
  <img src="https://raw.githubusercontent.com/Atem83/Youtube-Comment-Export/main/images/Excel comments sheet.png" alt="Excel comments sheet" style="width: 100%;">
</div>

<h2 align="center"> Features </h2>

- Download data from a YouTube channel
- Download comments from a YouTube channel
- Export the data and comments in Excel files in a nice format
- Light ou Dark theme according to your OS theme
- Import old saves, this way :
  - you can keep a more precise date of the comments
  - you can keep comments even if they have been deleted
  - sadly, it will not be possible to save downloading time because all the comments needs to be downloaded again

<h2 align="center"> Installation </h2>

<div align="center">

```
pip install Youtube-Comment-Export
```

[<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Atem83/Youtube-Comment-Export?&color=green&label=Source%20Code&logo=Python&logoColor=yellow&style=for-the-badge"  width="300">](https://github.com/Atem83/Youtube-Comment-Export/archive/refs/heads/main.zip)

</div>

<h2 align="center"> GUI Usage </h2>

```python
import ytComments

app = ytComments.App()
app.run()
```
<h2 align="center"> Python Usage </h2>

```python
import ytComments

channel_url = 'https://www.youtube.com/@GabbPiano'
path_save1 = r'C:\Users\User\Desktop\Save File 1.xlsx'
path_save2 = r'C:\Users\User\Desktop\Save File 2.xlsx'
path_save = [path_save1, path_save2]

yt = ytComments.yt_manager(channel_url, old_save=path_save)
yt.import_excel() # Import the old save data
yt.export_excel() # Export the data in Excel files

```

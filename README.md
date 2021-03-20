English | [简体中文](./README-zh-CN.md)

# Market-Helper 售货辅助器
*“As a manager of a shop, helping staffs and customers with a software can be great, right?”*

## Usage
Now many supermarkets, even small shops, have computers (and a barcode scanner) helping staffs and customers to shop easily.

But, alongside a computer, a software is also needed.

This is a simple but useful pal for your shop's computer.

You can use it to improve customers' shopping experience, staffs' work efficiency, and more.

## Why?
- Many ones choose to *pay for* a professional shopping software, but after that they still have no idea to use it easilly.
- This application avoids such a condition. You have **no need to pay** for this software, and it's easy to configure.
- Most of those professional softwares have *overloaded functions*, that is, there are things that are not needed, but you have to pay, to learn, and to suffer.
- However, this application **have no such pain**. It's light-weight, aim-focused, it's just for you.
- Professional also means *[proprietary](https://www.gnu.org/proprietary/proprietary.html)*. You lost yourself when using them.
- But this application is **[Free Software](https://www.gnu.org/)**, it serves only you, your business, and your customers.

## Install
- If your computer uses Windows, it's recommended to switch to a [GNU/Linux system](https://www.gnu.org/distros/free-distros.html). If you don't want, just read on.
  - (Optional) Make your system can auto-login.
  - In Windows, install *Python3* and a non-IE standalone *browser*.
  - Download a release of this repository, extract it to somewhere.
  - Create a **shortcut** for *main.py* by right-click-drag the file and select "Create shortcut".
  - After that, put both main.py file *shortcut* and browser *shortcut* (usually on desktop) to `Start Menu -> Startup` folder.
  - Configure your browser, set mainpage (or startup page) to `http://localhost:8101/`
  - Reboot the computer, now it runs your application automatically.
- If it's running GNU/Linux, then:
  - (Optional) Make your system can auto-login.
  - Ensure package *python3* and *firefox* is already installed.
  - Download a release of this repository, extract it to somewhere, remember location of the *main.py* file.
  - Edit the file `(user's home folder)/.bashrc` (or other autorun file depending on your environment), append a line after the file:
    - `python3 ~/path/to/main.py`
  - Reboot the computer, now it runs your application automatically

## Tips
- For barcode & price system:
  - First you need to do is to *record items* in your shop to database. Recommended way:
    - On computer, open this tool, ensure it is connected to a network, and get its IP address.
    - Open your phone, open Wlan Settings, connect to a network (WiFi) which your computer also joined.
    - Plug in your barcode scanner to your phone with an *OTG connector*.
    - On phone's browser, open `http://computerIP:8101/`, then open menu inside the webpage.
    - Scroll down, in "Manage" section, you can record your items. Scan a barcode, input item's name, unit, price, and click on Record button.
    - Take your phone and a parterner, just walk through your market/shop, record all your items.
  - Once you have your own database, it's time to copy the database to other computers. (Feature precast: on webpage side import database)
  - If an item your customers take have not been recorded, you can simply input the *price* of it.
  - After scanning customer's items, *Settle* the deal. Browser will give a print dialog for bill printing.

- For barcode & member system:
  - When input in barcode starts with a minus sign (-), it's considered as a "command". A letter following as the command type, after details, span with another minus...
  - "-a" means register for a *member*, syntax like `-a10010001000-Name` registers a member named `Name` with ID `10010001000`. ID can be phone number or other things.
  - After registering a member, a *member code* is provided. Customer just shot (not scan) the code with phone camera.
  - Once scan the member code with barcode scanner, this helper will treat current session as *member session* until "Settle".
  - In member session, you can *use credit* for one time, *credit* is given after one settlement according to how many the customer spent.
  - With this credit system, you can give often-comers some gifts. This is required by many shop/markets for far development.

## Support
If you wish to support this project, you can:
- Easiest, Star this repository;
- Or, help to promote this project;
- Even, if you have the ability, use Issue, Fork, Pull Request to help this project.
- If you want to sponsor, open an issue, the author may provide a method!

## Thanks
Thank you for your patience and supports! Wish this software can help you most!

class MarketHelper {
    constructor() {
        this.hiddenSection = document.querySelector('section.hidden');
        this.table = document.getElementById('items_table').querySelector('tbody');
        this.menu = document.getElementById('menu');
        this.menuOpened = false;
        this.manager = document.getElementById('manager');
        this.elemLog = document.getElementById('log');
        document.addEventListener('keyup', event => {
            if (event.key == 'Escape') this.toggleMenu();
        });
        this.inputBarcode = document.getElementById('input_barcode');
        this.inputBarcode.addEventListener('keyup', event => {
            if (event.key == 'Enter') this.input();
        });
        this.inputPrice = document.getElementById('input_price');
        this.inputPrice.addEventListener('keyup', event => {
            if (event.key == 'Enter') this.inputAsPrice();
        });
        this.inputCredits = document.getElementById('input_credits');
        this.inputCredits.addEventListener('keyup', event => {
            if (event.key == 'Enter') this.useCredits();
        });
        this.currentMember = '';
        this.memberCode = document.getElementById('member_code');
        this.elemSum = document.getElementById('sum');
        this.actions = [
            [i18N.get('Delete'), 'this.parentElement.parentElement.remove(); helper.calcSum();']
        ];
        this.actionSign = '-';
        this.apikey = '';
        fetch('/~?action=get_apikey').then(r => r.text()).then(t => {
            t = t.trim();
            this.apikey = t;
            fetch('/manager.html').then(r => r.text()).then(html => {
                this.manager.contentDocument.write(html.replace('%apikey%', t));
            });
        });
    }
    log(msg, type = 'normal') {
        this.elemLog.querySelectorAll('*').forEach(e => e.remove());
        if (msg == '') return '';
        let text = document.createElement('span');
        text.innerText = i18N.get('LogFormat').replace('%time%', new Date().toLocaleTimeString('en-US')).replace('%msg%', msg);
        text.classList.add(type);
        this.elemLog.appendChild(text);
        return msg;
    }
    shutdown() {
        fetch(`/~?apikey=${this.apikey}&action=shutdown`);
    }
    async getRecord(code) {
        const r = await fetch(`/~?apikey=${this.apikey}&action=get_record&code=${code}`);
        if (r.status == 200) {
            return await r.text();
        } else {
            return await Promise.reject(i18N.get('InvalidCode').replace('%code%', code));
        }
    }
    toggleMenu() {
        if (this.menuOpened) this.menu.style.top = '';
        else this.menu.style.top = '0';
        this.menuOpened = !this.menuOpened;
    }
    isActionCode(code) {
        return code[0] === this.actionSign;
    }
    addItem(record) {
        let info = record.split(',');   // Barcode, Name, Unit, Price
        let tr = document.createElement('tr');
        for (let i of info) {
            let td = document.createElement('td');
            td.innerText = i;
            tr.appendChild(td);
        }
        let actionButtons = document.createElement('td');
        for (let i of this.actions) {
            let a = document.createElement('a');
            a.href = 'javascript:';
            a.innerText = i[0];
            a.setAttribute('onclick', i[1]);
            actionButtons.appendChild(a);
        }
        tr.appendChild(actionButtons);
        this.table.appendChild(tr);
    }
    async doAction(code) {
        let info = code.slice(2).split(this.actionSign);
        switch (code[1]) {
            case '*':
            case '+':
                // Multiply last item
                let count = parseInt(info[0]) - (code[1] == '*' ? 1 : 0);
                if (this.table.lastChild == null) return;
                for (let i = 0; i < count; i++) {
                    let copy = this.table.lastChild.cloneNode(true);
                    this.table.append(copy);
                }
                this.log(i18N.get('MultiplyedCount').replace('%count%', count));
                this.calcSum();
                break;
            case 'a':
                // Register member
                // let member_code = btoa(info[0]).toUpperCase().replace('=', '$');    // Code39 have only one case for letters
                let member_code = info[0];  // Usually phone number
                fetch(`/~?apikey=${this.apikey}&action=write_member&member=${member_code},${info[1]},0`);
                this.memberCode.innerText = `*-A${member_code}*`;
                this.toggleMenu();
                break;
            case 'A':
                // Assign member
                let member_query_request = await fetch(`/~?apikey=${this.apikey}&action=get_member&id=${info[0]}`);
                if (member_query_request.status === 200) {
                    member_query_request.text().then(t => {
                        this.currentMember = t;
                        let member_info = t.split(',');
                        this.log(i18N.get('WelcomeMember').replace('%member%', member_info[1]).replace('%left_credits%', member_info[2]));
                        document.querySelector('.use_credit_form').style.display = 'table-row';
                        this.inputCredits.focus();
                    });
                } else {
                    this.log(i18N.get('MemberNotFound'), 'error');
                }
                break;
            case 'B':
                // Live barcode, i.e. from weight-defined items, lively generated barcode
                // Format should be: |-B|0123|-|01234567|, first is item type, second is price, 1 as $0.001
                this.getRecord(info[0]).then(record => {
                    this.addItem(record.replace(',0', `,${parseInt(info[1]) / 1000}`));
                    this.calcSum();
                }, error => this.log(error, 'error'));
                this.inputBarcode.value = '';
                this.inputBarcode.focus();
                break;
        }
    }
    useCredits() {
        let credits = parseFloat(this.inputCredits.value);
        let member_name = this.currentMember.split(',')[1];
        let left_credits = parseFloat(this.currentMember.split(',')[2]) - parseFloat(credits);
        let new_member_info = this.currentMember.split(',');
        new_member_info[2] = left_credits;
        fetch(`/~?apikey=${this.apikey}&action=write_member&member=${new_member_info.join(',')}`).then(r => r.text()).then(t => {
            this.log(i18N.get('UsedCredits').replace('%member%', member_name).replace('%left_credits%', left_credits));
            document.querySelector('.use_credit_form').style.display = '';
            this.currentMember = new_member_info.join(',');
            this.inputCredits.value = '';
            this.inputBarcode.focus();
        });
    }
    input() {
        let code = this.inputBarcode.value;
        if (this.isActionCode(code)) this.doAction(code);
        else this.getRecord(code).then(record => {
            this.addItem(record);
            this.calcSum();
        }, error => this.log(error, 'error'));
        this.inputBarcode.value = '';
        this.inputBarcode.focus();
    }
    inputAsPrice() {
        let price = this.inputPrice.value;
        this.addItem(`,${i18N.get('(Manual Input)')},${i18N.get('ForOne')},${price}`);
        this.inputPrice.value = '';
        this.calcSum();
        this.inputBarcode.focus();
    }
    calcSum() {
        let prices = this.table.querySelectorAll('tbody tr td:nth-child(4)');
        let sum = 0;
        prices.forEach(e => {
            let number = parseFloat(e.innerText);
            sum += isNaN(number) ? 0 : number;
        });
        this.elemSum.innerText = Math.round(sum * 100) / 100;
        return sum;
    }
    clear() {
        this.table.querySelectorAll('tr').forEach(e => e.remove());
        this.calcSum();
        this.currentMember = '';
        // this.log('');
    }
    hiddenAppendChild(element) {
        this.hiddenSection.querySelectorAll('*').forEach(e => e.remove());
        this.hiddenSection.appendChild(element);
    }
    settle() {
        let sum = this.calcSum();
        if (this.currentMember != '') {
            this.inputCredits.value = -sum;
            this.useCredits();
        }
        let iframe = document.createElement('iframe');
        iframe.src = '/paper_template.html';
        iframe.addEventListener('load', () => {
            let title = iframe.contentDocument.getElementById('title');
            // let title = iframe.contentDocument.querySelector('title');
            let table = iframe.contentDocument.getElementById('table');
            let description = iframe.contentDocument.getElementById('description');
            title.innerHTML = i18N.get('PaperTitle');
            description.innerHTML = i18N.get('PaperDescription').replace('%sum%', sum);
            let items = this.table.querySelectorAll('tr td:nth-child(2)');
            let units = this.table.querySelectorAll('tr td:nth-child(3)');
            let prices = this.table.querySelectorAll('tr td:nth-child(4)');
            for (let i = 0; i < items.length; i++) {
                let tr = document.createElement('tr');
                let td1 = document.createElement('td');
                td1.innerText = `${items[i].innerText} ${units[i].innerText}`;
                let td2 = document.createElement('td2');
                td2.innerText = prices[i].innerText;
                tr.appendChild(td1);
                tr.appendChild(td2);
                table.appendChild(tr);
            }
            iframe.contentWindow.print();
            this.clear();
        });
        this.hiddenAppendChild(iframe);
    }
    printMemberCode() {
        let code = this.memberCode.innerText;
        let iframe = document.createElement('iframe');
        let html = `<!doctype html>
        <html><head><style>
        @font-face { src: url('/css/ConnectCode39.ttf'); font-family: 'ConnectCode39'; }
        </style></head><body>
        <p style="font-size: 3em; font-family: 'ConnectCode39'; writing-mode: vertical-lr;">${code}</p>
        </body></html>`;
        this.hiddenAppendChild(iframe);
        iframe.contentDocument.write(html);
        iframe.contentWindow.print();
    }
}

var helper = new MarketHelper();

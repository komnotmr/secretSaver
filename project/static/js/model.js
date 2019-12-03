'use strict;'

class Model
{
    constructor() {
        // date + 3 days from today as default date
        this.defaultLifeTime = ( (d)=>{
            d.setDate(d.getDate() + 3);
            let _s = (_d) => { return _d < 10 ? `0${_d}` : `${_d}`; }
            return `${d.getFullYear()}-${_s(d.getMonth()+1)}-${_s(d.getDate())}`;
        })(new Date());
        // default alert message
        this.defaultAlert = "Input your message or secret code in textarea above";
        // users data
        this.data = ko.observable("");
        this.lifeTime = ko.observable(this.defaultLifeTime);
        // for alerts
        this.styleTypes = ["light", "dark", "danger"];
        // style id: 0 - proccess, 1 - waiting user, 2 - error
        this.styleId = ko.observable(1);
        this.alertMessage = ko.observable(this.defaultAlert);
        // setters styles for alert and button
        this.setAlertStyle = ko.pureComputed(()=>{
            return `alert alert-${this.styleTypes[this.styleId()]}`;
        });
        this.setButtonStyle = ko.pureComputed(()=>{
            return `btn btn-${this.styleTypes[this.styleId()]}`;
        });
    }
    // setting alert and class types 
    setSituation(id, msg='') {
        if (id >= this.styleTypes.length)
            return;
        this.styleId(id);
        this.alertMessage(msg);        
    }
    // check user's data is code
    isCode() {
        let data = this.data().trim();
        if (data.length === 0) 
            return false;
        //key like xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        return /^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$/.test(data);
    }
    
    inputIsCorrect() {
        // check message or code
        if (this.data().length === 0
            || this.data().trim().length === 0) {
                this.setSituation(2, 'Input data is empty');
        return false;
        }
        // if data exists check that is code
        // if this is message - check date else send code
        if (this.isCode()) 
            return true;
        // check lifeTime
        if (this.lifeTime().length === 0) {
            this.lifeTime(this.defaultLifeTime);
            this.setSituation(2, 'Please, choice life time message');
            return false;
        }

        let d = Date.parse(this.lifeTime());
        if (d < Date.now()) {
                if (d === this.defaultLifeTime)
                    this.setSituation(2, 'You need to choice life time message');
                else
                    this.setSituation(2, 'You need to choice life time later then tomorrow');
            return false;
        }
        return true;
    }

    send() {
        self = this;
        // check user input
        if(!this.inputIsCorrect()) return;
        $.ajax({
                method: 'POST',
                url: '/',
                data: {
                    data: self.isCode() ? self.data().trim() : self.data(),
                    lifeTime: self.lifeTime()
                }
            }).done((msg)=>{
                console.log(msg);
                if (msg.errors.length > 0) {
                    self.setSituation(2, msg.errors[0])
                } else {
                    self.data(msg.data)
                    self.setSituation(1, this.defaultAlert)
                }
            }).fail((jqXRH, textStatus)=>{
                console.log(textStatus);
                self.setSituation(2, 'Server error, try later');
            });
    }
}

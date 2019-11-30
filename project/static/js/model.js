'use strict;'

class Model
{
    constructor() {
        this.data = ko.observable("");
        this.lifeTime = ko.observable("");
        this.styleTypes = ["light", "dark", "danger"];
        this.styleId = ko.observable(1);
        this.defaultAlert = "Input your message or secret code in textarea above";
        this.alertMessage = ko.observable(this.defaultAlert);
        this.setAlertStyle = ko.pureComputed(()=>{
            return `alert alert-${this.styleTypes[this.styleId()]}`;
        });
        this.setButtonStyle = ko.pureComputed(()=>{
            return `btn btn-${this.styleTypes[this.styleId()]}`;
        });
    }

    send() {
        self = this;
        self.styleId(0);
        $.ajax({
                method: 'POST',
                url: '/',
                data: {
                    data: self.data(),
                    lifeTime: self.lifeTime()
                }
            }).done((msg)=>{
                console.log(msg);
                if (msg.errors.length > 0) {
                    self.styleId(2);
                    self.alertMessage(msg.errors[0]);
                } else {
                    self.data(msg.data)
                    self.styleId(1);
                    self.alertMessage(this.defaultAlert);
                }
            }).fail((jqXRH, textStatus)=>{
                console.log(textStatus);
                self.alertMessage('Server error, try later');
                self.styleId(2);
            });
    }
}

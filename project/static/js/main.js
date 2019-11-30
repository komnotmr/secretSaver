console.log('script connected');
var model = null;

function init()
{
    ko.applyBindings(model = {
        textMessage: ko.observable("Input sercet message"),
        textCode: ko.observable("")
    });
}

function sendMessage(self)
{
    self.className = "btn btn-light";
    setTimeout(()=>{
        $.ajax({
            method: 'POST',
            url: '/',
            data: {
                k1: 'v1',
                k2: 'v2'
            }
        }).done((msg)=>{
            console.log(msg);
            self.className = "btn btn-dark";
            model.textMessage('');
            model.textCode('Asd8ddaN4')
        }).fail((jqXRH, textStatus)=>{
            console.log(textStatus);
            self.className = "btn btn-danger"
        });
    }, 2000);
}
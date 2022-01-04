function addTicket(ticketId ,name, passport, telephone, ticketClass, price) {
    event.preventDefault()
    console.log(ticketId)
    // promise
    fetch('/api/add-ticket', {
        method: 'post',
        body: JSON.stringify({
            'ticket_id': ticketId,
            'passport': passport,
            'name': name,
            'telephone': telephone,
            'ticket_class': ticketClass,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data) {
        location.reload()
    })
}

function pay() {
    if (confirm('Ban chac chan thanh toan khong?') == true) {
        fetch('/api/pay', {
            method: 'post'
        }).then(function(res) {
            return res.json()
        }).then(function(data) {
            if (data.code === 200)
                location.reload()
            else
                console.log(data)
        })
    }
}
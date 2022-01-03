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
        let tableRow = document.getElementById('table')
        console.log(data)
        tableRow.innerHTML = tableRow.innerHTML + `<tr>
        <td>${data.name}</td>
        <td>${data.passport}</td>
        <td>${data.telephone}</td>
        <td>${data.ticket_class}</td>
        <td>${data.price}</td>
    </tr>`
    })
}
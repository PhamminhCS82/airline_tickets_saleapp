function addTicket(name, passport, telephone, ticketClass, price) {
    event.preventDefault()

    // promise
    fetch('/api/add-ticket', {
        method: 'post',
        body: JSON.stringify({
            'passport': passport,
            'name': name,
            'telephone': telephone,
            'ticket-class': ticketClass,
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
    </tr>`
    })
}
window.onload = () => {
    document.getElementById('returnDay').disabled = true;
}

const handleChange = (src) => {
    if(src.value === 'oneTrip')
        document.getElementById('returnDay').disabled = true;
    else
        document.getElementById('returnDay').disabled = false;
}


function attemptSearchByDate(){
    let d = document.getElementById('input_date').value;
    let m = document.getElementById('input_month').value;
    let y = document.getElementById('input_year').value;

    if(d.length == 1){
        d = `0${d}`;
    } if(m.length == 1){
        m = `0${m}`;
    } if(y.length == 1){
        y = `0${y}`;
    }

    compiledDate = `${y}-${m}-${d}`;

    if(!dateInDatabase(d,m,y)){
        document.getElementById('date_input_form').classList.add('animate-shake');
        setTimeout(function () {
            document.getElementById('date_input_form').classList.remove('animate-shake');
        }, 400);
    } else {
        while(active_dates_array.indexOf(compiledDate) == -1){
            extendFile();
        }
        let yOffset = -140;
        let element = document.getElementById(compiledDate);
        let yPos = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
        window.scrollTo({top: yPos, behavior: 'smooth'});
    }
}

function dateInDatabase(d,m,y){
    return global_dates_only_array.indexOf(`${y}-${m}-${d}`) != -1;
}

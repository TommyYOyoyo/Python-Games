
let isAP = false;

setInterval(clock, 1000)

function clock(){

    let date = new Date();

    document.getElementById('myClock').innerHTML = update(date);

    function update(date){
        let hour = date.getHours();
        let minute = date.getMinutes();
        let seconds = date.getSeconds();

        let AoP = "AM";

        console.log(isAP);
        
        if (seconds < 10){
            seconds = '0'+seconds
        }
        if (minute < 10){
            minute = '0'+minute
        }

        if (isAP == true){
            hour >= 12 ? AoP = "PM" : AoP = "AM";
            hour = (hour % 12 ) || 12;
        }

        let day = date.getDate();

        if(day < 10){
            day = '0'+day;
        }
        
        let month = date.getMonth() + 1;
        let year = date.getFullYear();

        if(month < 10){
            month = '0'+month;
        }

        date = `${year}/${month}/${day}`
        document.getElementById("myDate").innerHTML = date;
        if (isAP == false){
            return `${hour}:${minute}:${seconds}`
        }
        else if (isAP == true){
            document.getElementById("APlabel").innerHTML = AoP
            return `${hour}:${minute}:${seconds}`
        }
    }
    
}

document.getElementById("changeFormat").onclick = function(){
    if (isAP == false){
        isAP = true;
        document.getElementById("changeFormat").innerHTML = "24H"
    }
    else if (isAP == true){
        isAP = false;
        document.getElementById("APlabel").innerHTML = "";
        document.getElementById("changeFormat").innerHTML = "AM/PM"
    }
}

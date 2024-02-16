$(window).ready(function(){
    $(window).scroll(function(){
        if($(this).scrollTop()){
            $('.gohead').fadeIn(); // ẩn element có class là gohead 
        }
        else{
            $('.gohead').fadeOut();// hiện element có class là gohead 
        }
    });
    $('.gohead').click(function(){ 
        $('html, body').animate({scrollTop:0},2000); // chỉnh animate scrollTop chạy 2s 
    })
    var wow = new WOW(
        {
            boxClass:     'wow',      
            animateClass: 'animate__animated', 
            offset:       0,          
            mobile:       true,       
            live:         true,      
            callback:     function(box) {
                
            },
            scrollContainer: null,   
            resetAnimation: true,     
        }
    );
    wow.init();
});

function bRCL(obj){
    var c=obj.value;
    var d=document.getElementById("but");
    if(obj.value==="TURN ON"){
        document.body.style.backgroundColor="#c8d6e5";
        obj.value="TURN OFF";
        d.style.backgroundColor="#c8d6e5";
        d.style.border="none"
        return;
    }
    if(obj.value==="TURN OFF"){
        document.body.style.backgroundColor="#fff";
        obj.value="TURN ON";
        d.style.backgroundColor="#fff";
        d.style.border="1px solid #000"
        return;
    }
}
function changeMap(obj){
    var a=obj.value;
    var b=document.querySelector(".MAP > iframe");
    var c=document.querySelector(".contact > #address > span");
    b.classList.add("big");
    if(a==="2"){
         b.src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3918.925119729195!2d106.6749189145894!3d10.817042392293967!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x317528e1f241211f%3A0xc9ef195798144b1f!2zVHLGsOG7nW5nIMSQ4bqhaSBo4buNYyBN4bufIFRQLkhDTSAtIEPGoSBz4bufIE5ndXnhu4VuIEtp4buHbQ!5e0!3m2!1svi!2s!4v1658469460822!5m2!1svi!2s";
         c.innerHTML=`<i class="fa-solid fa-location-dot"></i> 371 Nguyễn Kiệm, phường 3, Quận Gỏ Vấp,TPHCM `
         return ;
    }
    if(a==="1"){
        b.src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3919.456658453734!2d106.68817011458903!3d10.776293992321628!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31752f3ae35e3725%3A0x20c5174a47f97be3!2zVHLGsOG7nW5nIMSQ4bqhaSBo4buNYyBN4bufIFRQLkhDTSAtIEPGoSBz4bufIDE!5e0!3m2!1svi!2s!4v1658469791524!5m2!1svi!2s";
        c.innerHTML=`<i class="fa-solid fa-location-dot"></i>  97 Võ Văn Tần, phường 6, Quận 3, TPHCM `
        return ;
   }
}
       let names=["Thiết kế web" ,"Tin học Mos","Data Science"];

function auto(obj){
    let b=document.getElementById("network"); 
    var a = document.getElementById("input");
    let i=0;
    let listItem;
    let items  = document.querySelectorAll("li.list-item");
        for(let i=0;i<items.length;i++){
            items[i].remove("li");
        }
        while(a.value != names[i] && a.value!="" && i<3){
            var c=names[i].substring(0,a.value.length).toLowerCase();
            var d=a.value.toLowerCase();
            if(d===c){
                listItem = document.createElement("li");
                listItem.classList.add("list-item");
                listItem.innerHTML=names[i];
                document.querySelector("ul.list").appendChild(listItem);  
                listItem.setAttribute("onclick", "disPlayNames('" + names[i] + "')");
            }
            i++;
        }

}

 function disPlayNames(value){
    var a=document.getElementById("input");
    a.value=value;
    var listItem=document.getElementsByClassName("list-item")
   for(var i=0;i<listItem.length;i++){
        listItem[i].style.display="none";
   }
    
}
    function init(){
        let b=document.getElementById("network"); 
        var a = document.getElementById("input");
        var c=document.querySelector("select.list").value;
        if(a.value==="Thiết kế web" || c=="14"){
            b.setAttribute("href", "http://127.0.0.1:5501/html/trang2.html"); // thiết lập địa chĩ cho nút
        }
        else if(a.value==="Tin học Mos" || c=="11"){
            b.setAttribute("href", "http://127.0.0.1:5501/html/trang3.html");
        }
        else if(a.value==="Data Science" || c=="12"){
            b.setAttribute("href", "http://127.0.0.1:5501/html/trang4.html");
        }
        else {
            b.setAttribute("href", "#");
        }
    }
var dem=0;
function thanhmenu(obj)
{
    var a=document.getElementById("cha");
    if(dem>=1)
    {
        a.style.display="none";
        dem=0;
    }  
    else
    {
        a.style.display="block";
        dem++;
    }
}
var demcon=0;
function thanhmenucon(obj){
    var b=document.getElementById("con");
    if(demcon>=1)
    {
        
            b.style.display="none";
            demcon=0;
    }  
    else
    {
        
            b.style.display="block";
            demcon++;
    }
}
var demcon1=0;
function thanhmenucon1(obj){
    var c=document.getElementById("ae-con");
    if(demcon1>=1)
    {
        
            c.style.display="none";
            demcon1=0;
    }  
    else
    {
        
            c.style.display="block";
            demcon1++;
    }
}

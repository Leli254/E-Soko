/* a script that  displays pickup location form field if shipping method is selected as "Pickup" in PickupStationForm of orders.forms
    and hides it if shipping method is selected as "Delivery" in PickupStationForm of orders.forms
>*/


<script>
function showDiv(select){
   if(select.value=='Pickup'){
      document.getElementById('hidden_div').style.display = "block";
   } else{
      document.getElementById('hidden_div').style.display = "none";
   }
}
</script>
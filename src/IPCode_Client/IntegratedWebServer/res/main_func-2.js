/*
    File name: main_func-2.js
    Author: LiuJiewenTT(on Github.com)
    Description:
        This script is about unsorted functions.
    Rights Declaration:
        The codes have something taken from the Internet. External sourced codes may be edited and only belong to the license mentioned in the corresponding part. If not explicitly indicated, codes will be under the license of this project.
*/

// ________________
// Part 1
function js_2_onload(){
    var func_name='onload'
    checkNewestStatus()
    return;
}

// ________________ End of Part 1
// ________________
// Part 2

function checkNewestStatus(){
    var currentIPv6Address = document.getElementById("code_ipv6_address").innerText
    var currentIPv6Prefix = document.getElementById("code_ipv6_prefix").innerText
    console.log("[checkNewestStatus]:Begin")
    if( currentIPv6Address != null ){
        var code_ipv6_address = document.getElementById("code_ipv6_address")
        var status_icon_ipv6_address = document.getElementById("status_icon_ipv6_address")
        if( code_ipv6_address.innerText == "None" ){
            console.log("code_ipv6_address is None")
            // window.alert(currentIPv6Address)
            // var span_ipv6_address = document.getElementById("span_ipv6_address")
            var del_ipv6_address = document.createElement("del")
            del_ipv6_address.appendChild(code_ipv6_address.cloneNode(deep=true))
            // span_ipv6_address.replaceChild(del_ipv6_address, code_ipv6_address)
            code_ipv6_address.parentNode.replaceChild(del_ipv6_address, code_ipv6_address)
            status_icon_ipv6_address.style.background = "red"
        }
        else {
            status_icon_ipv6_address.style.background = "green"
        }
    }
    if( currentIPv6Prefix != null ){
        var code_ipv6_prefix = document.getElementById("code_ipv6_prefix")
        var status_icon_ipv6_prefix = document.getElementById("status_icon_ipv6_prefix")
        if( code_ipv6_prefix.innerText == "None" ){
            console.log("code_ipv6_prefix is None")
            // window.alert(currentIPv6Prefix)
            var del_ipv6_prefix = document.createElement("del")
            del_ipv6_prefix.appendChild(code_ipv6_prefix.cloneNode(deep=true))
            code_ipv6_prefix.parentNode.replaceChild(del_ipv6_prefix, code_ipv6_prefix)
            status_icon_ipv6_prefix.style.background = "red"
        }
        else {
            status_icon_ipv6_prefix.style.background = "green"
        }
    }
    console.log("[checkNewestStatus]:End")
}

// ________________ End of Part 2
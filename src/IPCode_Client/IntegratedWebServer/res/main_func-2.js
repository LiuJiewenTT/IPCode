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

function checkNewestStatus(){
    var currentIPv6Address = document.getElementById("code_ipv6_address").innerText
    var currentIPv6Prefix = document.getElementById("code_ipv6_prefix").innerText
    if( currentIPv6Address != null ){
        window.alert(currentIPv6Address)
    }
    if( currentIPv6Prefix != null ){
        window.alert(currentIPv6Prefix)
    }
}

// ________________ End of Part 1
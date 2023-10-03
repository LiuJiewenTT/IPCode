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
    // let func_name='onload'
    checkNewestStatus()
}

function wrap_an_element(element, wrapper_label){
    let wrapper = document.createElement(wrapper_label)
    wrapper.appendChild(element.cloneNode(deep=true))
    element.parentNode.replaceChild(wrapper, element)
}

function wrap_del_an_element(element){
    wrap_an_element(element, "del")
}

// ________________ End of Part 1
// ________________
// Part 2

function checkNewestStatus(){
    let span_ipv6_address = document.getElementById("span_ipv6_address")
    let currentIPv6Address = document.getElementById("code_ipv6_address").innerText
    let currentIPv6Prefix = document.getElementById("code_ipv6_prefix").innerText
    console.log("[checkNewestStatus]:Begin")
    if( currentIPv6Address != null ){
        let code_ipv6_address = document.getElementById("code_ipv6_address")
        let status_icon_ipv6_address = document.getElementById("status_icon_ipv6_address")
        let if_newest = false
        // Show status
        if( code_ipv6_address.innerText === "None" ){
            console.log("[Warning]: code_ipv6_address is None")
            wrap_del_an_element(code_ipv6_address)
            status_icon_ipv6_address.style.background = "red"
        }
        else {
            status_icon_ipv6_address.style.background = "green"
            let storedIPv6Address = localStorage.getItem("IPv6_Address")
            if( storedIPv6Address !== currentIPv6Address ){
                console.log("[Info]: New IPv6_Address")
                if_newest = true
                // storedIPv6Address = currentIPv6Address
                localStorage.setItem("IPv6_Address", currentIPv6Address)
            }
        }
        if( if_newest === true ){
            // let badge_newest = document.getElementById("badge_newest_ipv6_address")
            let badge_newest = span_ipv6_address.getElementsByClassName("Badge_Newest")
            console.log(badge_newest!=null)
            badge_newest.item(0).removeAttribute("hidden")
        }
    }
    if( currentIPv6Prefix != null ){
        let code_ipv6_prefix = document.getElementById("code_ipv6_prefix")
        let status_icon_ipv6_prefix = document.getElementById("status_icon_ipv6_prefix")
        let if_newest = false
        // Show status
        if( code_ipv6_prefix.innerText === "None" ){
            console.log("[Warning]: code_ipv6_prefix is None")
            wrap_del_an_element(code_ipv6_prefix)
            status_icon_ipv6_prefix.style.background = "red"
        }
        else {
            status_icon_ipv6_prefix.style.background = "green"
            let storedIPv6Prefix = localStorage.getItem("IPv6_Prefix")
            if( storedIPv6Prefix !== currentIPv6Prefix ){
                console.log("[Info]: New IPv6_Prefix")
                if_newest = true
                // storedIPv6Prefix = currentIPv6Prefix
                localStorage.setItem("IPv6_Prefix", currentIPv6Prefix)
            }
        }
    }
    console.log("[checkNewestStatus]:End")
}

// ________________ End of Part 2
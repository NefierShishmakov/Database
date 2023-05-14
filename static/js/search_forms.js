let error = document.getElementById('error');
let send_button = document.getElementById('send');
let clear_button = document.getElementById('clear');
let main_form = document.getElementById('main_form');

function regex_check(element) {
    let pattern = element.pattern;
    if (pattern != "") {
        let re = new RegExp(pattern);
        if (!re.test(element.value)) {
            return false;
        }
    }
    return true;
}

function set_error_text(text) {
    error.classList.remove('success');
    error.classList.add('error');
    error.textContent = text;
}

function is_interval_section(element) {
    return element.id.search("interval") != -1;
}

function validate_interval(interval_element) {
    let from;
    let until;

    for (element of interval_element.children) {
        if (element.name == "from") {
            from = element;
        } else if (element.name == "until") {
            until = element;
        }
    }

    if (until.value == "" && from.value == "") {
        return true;
    }

    if ((until.value != "" && from.value == "") || (until.value == "" && from.value != "")) {
        set_error_text("All inputs of " + interval_element.id + " must be filled");
        return false;
    }

    if (!regex_check(from)) {
        set_error_text(from.name + " of " + interval_element.id + " is incorrect");
        return false;
    }

    if (!regex_check(until)) {
        set_error_text(until.name + " of " + interval_element.id + " is incorrect");
        return false;
    }

    let from_compare;
    let until_compare

    if (!isNaN(Number(from.value))) {
        from_compare = Number(from.value);
        until_compare = Number(until.value);
    } else {
        from_compare = new Date(from.value);
        until_compare = new Date(until.value);
    }

    console.log(from_compare + "\n" + until_compare);

    if (from_compare > until_compare) {
        set_error_text("The value of from must be equal or less then value of until");
        return false;
    }

    return true;
}

function validate_input(input) {
    if (!regex_check(input)) {
        set_error_text(input.name + " is incorrect");
        return false;
    }

    return true;
}

function is_not_empty_input(element) {
    return element.type != "checkbox" && element.nodeName == "INPUT" && element.value != "";
}

function validate(curr_form) {
    for (element of curr_form.children) {
        if (is_interval_section(element) && !validate_interval(element)) {
            return false;
        } else if (is_not_empty_input(element) && !validate_input(element)) {
            return false;
        }
    } 

    return true;
}

clear_button.onclick = () => {
    Array.from(main_form.children).map(
    (element) => {
    if (element.nodeName == "INPUT") {
        element.value = "";
    }
    if (element.type == "checkbox") {
        element.checked = false;
    }
    if (is_interval_section(element)) {
        for (el of element.children) {
            if (el.nodeName == "INPUT") {
                el.value = "";
            }
        }
    }
    });

    error.textContent = "";
}

function get_result_json_object(main_form) {
    let data = new Object();

    Array.from(main_form.children).map(
        (element) => {
        if (element.type == "checkbox") {
            if (element.checked) {
                data[element.name] = 'true';
            }
        } else if (element.id == "some" && element.value != "") {
            let result_array = element.value.split(", ");
            data[element.name] = "";
            
            for (el of result_array) {
                data[element.name] += (el + "_");
            }

            data[element.name] = data[element.name].slice(0, -1);
        } else if ((element.nodeName == "INPUT" || element.nodeName == "SELECT")  && element.value != "") {
            data[element.name] = element.value
        } else if (is_interval_section(element)) {
            let isFilled = true;

            for (el of element.children) {
                if (el.nodeName == "INPUT" && el.value == "") {
                    isFilled = false;
                    break;
                }
            }

            if (isFilled) {
                let key = element.id.substring(element.id.indexOf("_") + 1);
                data[key] = "";
                
                for (el of element.children) {
                    if (el.nodeName == "INPUT") {
                        data[key] += (el.value + "_");
                    }
                }
                data[key] = data[key].slice(0, -1);
            }
        }
    });

    return data;
}

function get_result_url(params) {
    let location = '' + window.location;
    location = location.substring(location.lastIndexOf("/") + 1);
    return '/search_forms/' + location + '_render_result?' + params.toString();
}

send_button.addEventListener('click', function () {
    if (validate(main_form)) {
        const params = new URLSearchParams(get_result_json_object(main_form));
        let url = get_result_url(params);
        window.location = window.location.origin + url;
    }
});
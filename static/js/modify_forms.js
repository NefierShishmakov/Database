let error = document.getElementById('error');
let send_button = document.getElementById('send');
let clear_button = document.getElementById('clear');
let mode_buttons = document.getElementsByName("btns");
let curr_mode = 'add';
let data_forms = document.getElementsByTagName('form');
let curr_form = data_forms[0];

let selectMode = (mode) => {
    if (mode == 0) curr_mode = 'add';
    if (mode == 1) curr_mode = 'update';
    if (mode == 2) curr_mode = 'delete';

    curr_form = data_forms[mode];
};

Array.from(mode_buttons).map(
    (button, index) => {
        
button.onclick = (() => {
    return () => {
        console.log('here');
        let forms = Array.from(document.getElementsByName('form')).map(
            (element) => {element.classList.add('hidden-form');
                            return element;
                            }
                );
        forms[index].classList.remove('hidden-form');
        selectMode(index);
        Array.from(curr_form.children).map(
            (element) => {
            if (element.nodeName == "INPUT" && element.type == "checkbox") {
                element.checked = false;
            }

            if (element.nodeName == "INPUT" && element.type != "checkbox") {
                element.value = "";
            }
        });
        error.textContent = "";
        console.log(curr_mode);
    } 
    
})();
    }
)

function regex_check(element) {
    let pattern = element.pattern;
    let re = new RegExp(pattern);
    if (!re.test(element.value)) {
        return false;
    }
    return true;
}

function all_regex_correct(curr_form) {
    for (element of curr_form.children) {
        if (element.nodeName == "INPUT" && element.type == "text") {
            if (!regex_check(element)) {
                error.classList.remove('success');
                error.classList.add('error');
                error.textContent = element.name + " is incorrect";
                return false;
            }
        }
    }
    return true;
}

function validate(curr_form) {
    if (curr_mode == 'add') {
        for(element of curr_form.children) {
            if (element.nodeName == "INPUT" && element.type != "checkbox") {
                if (element.value == "") {
                    error.classList.remove('success');
                    error.classList.add('error');
                    error.textContent = "All forms must be filled";
                    return false;
                }
            }
        }

        if (!all_regex_correct(curr_form)) {
            return false;
        }

        return true;
    } else if (curr_mode == 'delete') {
        let count = 0;
        for (element of curr_form.children) {
            if (element.type == "checkbox" || element.nodeName == "SELECT") {
                count += 1;
            }
            
            if (element.nodeName == "INPUT" && element.type != "checkbox" && element.value != "") {
                count += 1;
                if (element.type == "text" && !regex_check(element)) {
                    error.classList.remove('success');
                    error.classList.add('error');
                    error.textContent = element.name + " is incorrect";
                    return false;
                }
            }
        }

        if (count == 0) {
            error.classList.remove('success');
            error.classList.add('error');
            error.textContent = "At least one form must be filled";
            return false;
        }
        return true;
    } else if (curr_mode == 'update') {
        let id_element = curr_form.children[1];
        if (id_element.value == "") {
            error.classList.remove('success');
            error.classList.add('error');
            error.textContent = "Field " + id_element.name + " must be filled";
            return false;
        }

        let count = 0;
        for (let i = 1; i < curr_form.children.length; ++i) {
            let element = curr_form.children[i];
            if (element.type == "checkbox" || element.nodeName == "SELECT") {
                count += 1;
            }

            if (element.nodeName == "INPUT" && element.type != "checkbox" && element.value != "") {
                count += 1;
                if (element.type == "text" && !regex_check(element)) {
                    error.classList.remove('success');
                    error.classList.add('error');
                    error.textContent =  element.name + " is incorrect";
                    return false;
                }
            }
        }
        
        if (count <= 1) {
            error.classList.remove('success');
            error.classList.add('error');
            error.textContent =  "At least one form with id must be filled";
            return false;
        }
        return true;
    }
}

clear_button.onclick = () => {
    Array.from(curr_form.children).map(
    (element) => {
    if (element.nodeName == "INPUT") {
        element.value = "";
    }
    if (element.type == "checkbox") {
        element.checked = false;
    }
    });
    error.textContent = "";
}

send_button.addEventListener('click', function () {
    if (validate(curr_form)) {
        let data = new Object();
        let location = '' + window.location;
        data['type'] = curr_mode;
        data['table_name'] = location.substring(location.lastIndexOf("/") + 1);
        Array.from(curr_form.children).map(
            (element) => {
            if (element.type == "checkbox") {
                let value = 'true';
                if (!element.checked) {
                    value = 'false';
                }
                data[element.name] = value;
            }

            if ((element.nodeName == "INPUT" || element.nodeName == "SELECT") && element.type != "checkbox" && element.value != "") {
                if (isNaN(Number(element.value))) {
                    data[element.name] = element.value;
                } else {
                    data[element.name] = Number(element.value);
                }
            }
        });
        fetch('/modify_forms/modify_tables', {
            headers : {
                'Content-Type' : 'application/json'
            },
            method : 'POST',
            body : JSON.stringify(data)
        })
        .then(function (response) {
            if (response.ok) {
                response.json()
                .then(function(response) {
                    let str_response = response['response'];
                    if (str_response == 'Success') {
                        error.classList.remove('error');
                        error.classList.add('success');
                    } else {
                        error.classList.remove('success');
                        error.classList.add('error');
                    }

                    error.textContent = str_response;
                });
            }
            else {
                throw Error ('Something went wrong');
            }
        })
        .catch(function (error) {
            console.log(error);
        });
    }
});
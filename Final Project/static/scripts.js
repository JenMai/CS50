/*
 * Add task to database 
 * Prepare objects for it
 */ 
function new_task(){
    $('#addTask').submit(function(event) {

            if (event.isDefaultPrevented())                                             // prevent from sending anything if form is invalid: 
                return false                                                            // http://1000hz.github.io/bootstrap-validator/#validator-events

            var task = $('#task').val().replace(/['"]/g,"\\'").replace(/[#+-]/g,'');    // prevent some character issues
            var minute = parseInt($('#minute').val());
            
            if ($('#hour').val() == '')                                                 // check if hour is empty (form is optionnal)
                var hour = 0;
            else
                var hour = parseInt($('#hour').val());
            
            var minleft = (hour * 60) + minute;
            
            var objective = str_time(hour, minute);                                     // format display for sheet

            if ($('#goal').val() == '')                                                 // check if goal is empty (form is optionnal)
                var goal = 'None';
            else
                var goal = $('#goal').val().replace(/['"]/g,"\\'").replace(/[#+-]/g,'');
            
            var addData = $.ajax({                                                      // send via POST to Flask (somehow considered as JSON still?)
              url: '/add',
              method: 'POST',
              data: "{" + "'task' : " + "'" + task + "'"
                        + ", 'objective' : " + "'" + objective + "'"
                        + ", 'minute' : " + minleft 
                        + ", 'goal' : " + "'" + goal + "'" + "}",
              dataType: 'text',
              success: function (data) {
                    window.location = "/";
                }
            });
            
            addData.fail(function( jqXHR, textStatus, errorThrown ) {
            alert( 'Error: ' + textStatus + errorThrown )
            });
            
            event.preventDefault();
    });
};

/*
 * Reset 'done' timer from index
 */ 
function reset_done(task_id) {
    $(document).ready(function () {
        var taskID = parseInt(task_id);
        var delData= $.ajax({                                                            // send which task id is concerned
                      url: '/',
                      method: 'POST',
                      data: "{" + "'action' : " + 1
                                + ", 'taskID' : " + taskID + "}",
                      dataType: 'text',
                      success: function (data) {
                            location.reload();
                        }
                    });
                    
                    delData.fail(function( jqXHR, textStatus, errorThrown ) {
                    alert( 'Error: ' + textStatus + errorThrown )
                   });
    });
};

/*
 * Delete task from index
 */ 
function delete_task(task_id) {
    $(document).ready(function () {
        var taskID = parseInt(task_id);
        var delData= $.ajax({                                                            // send which task id is concerned
                      url: '/',
                      method: 'POST',
                      data: "{" + "'action' : " + 0
                                + ", 'taskID' : " + taskID + "}",
                      dataType: 'text',
                      success: function (data) {
                            location.reload();
                        }
                    });
                    
                    delData.fail(function( jqXHR, textStatus, errorThrown ) {
                    alert( 'Error: ' + textStatus + errorThrown )
                   });

    });
};


/*
 * Event listeners / form for subgoal page
 */ 
function goal_list(){
    $(document).ready(function () {
        
        $('#subForm').hide();
        
        $('#addbtn').click(function() {                                                  // display or hide sub-goal form
            $('#subForm').toggle();
            
        });
       
        $('#addSubgoal').submit(function(event) {
            if (event.isDefaultPrevented())
                return false
            
            var subgoal = $('#subgoal').val().replace(/['"]/g,"\\'").replace(/[#+-]/g,'');// prevent some character issues
            
            var getSub = $.ajax({
            method: 'POST',
            data: "{" + "'action' : " + 1
                    + ", 'taskID' : " + parseInt($('#currentTaskID').html())
                    + ", 'subgoal' : " + "'" + subgoal + "'" + "}",
            dataType: 'text',
            success: function (data) {
                    location.reload();
                }
            });

            getSub.fail(function( jqXHR, textStatus, errorThrown ) {
                alert( 'Error: ' + textStatus + errorThrown )
            });
            
            event.preventDefault();
        });
        
        var subChecked = []                                                             // prepare array for checked subgoals


        $('#goals .crossbtn').click(function (){                                        // subgoals to mark as done
            $('input[type=checkbox]').each(function () {
                if (this.checked)                                                       // push in array every box checked after event
                    subChecked.push(parseInt($(this).val()));
            });
            
            var subData = $.ajax({
              method: 'POST',
              data: "{" + "'action' : " + 2
                     + ", 'subgoalsID' : " + "[" + subChecked + "]" + "}",
              dataType: 'text',
              success: function (data) {
                    location.reload();
                }
            });
            
            subData.fail(function( jqXHR, textStatus, errorThrown ) {
            alert( 'Error: ' + textStatus + errorThrown )
            });
        });

        $('#goals .delbtn').click(function (){                                          // same as above, when delete is clicked
            $('input[type=checkbox]').each(function () {
                if (this.checked)
                    subChecked.push(parseInt($(this).val()));
            });
            
            var subData = $.ajax({
              method: 'POST',
              data: "{" + "'action' : " + 0
                     + ", 'subgoalsID' : " + "[" + subChecked + "]" + "}",
              dataType: 'text',
              success: function (data) {
                    location.reload();
                }
            });
            
            subData.fail(function( jqXHR, textStatus, errorThrown ) {
            alert( 'Error: ' + textStatus + errorThrown )
            }); 
        });
    });
};

/*
 * Event listeners / form for reference page (similar to goal)
 */ 
function reference_list(){
    $(document).ready(function () {
        
        $('#refForm').hide();
        
        $('#addbtn').click(function() {
            $('#refForm').toggle();
            
        });
       
        $('#addRef').submit(function(event) {
            if (event.isDefaultPrevented())
                return false
            
            var refTitle = $('#refTitle').val().replace(/['"]/g,"\\'").replace(/[#+-]/g,'');

            shortener = $.ajax({                                                        // use Google's URL shortener ( to set: API_KEY)
                url: 'https://www.googleapis.com/urlshortener/v1/url?shortUrl=http://goo.gl/fbsS&key=AIzaSyBky553Iel_8tqqawewCiZUQ01jaqSj3VM',
                type: 'POST',
                contentType: 'application/json; charset=utf-8',
                data: '{ longUrl: "' + $('#refLink').val() +'"}',
                dataType: 'json',
                success: function(data) {
                    var result = data["id"]
                    
                    var getRef = $.ajax({
                    method: 'POST',
                    data: "{" + "'action' : " + 1
                            + ", 'taskID' : " + parseInt($('#currentTaskID').html())
                            + ", 'refTitle' : " + "'" + refTitle + "'"
                            + ", 'link' : " + "'" + result + "'" + "}", 
                    dataType: 'text',
                    success: function (data) {
                            location.reload();
                            console.log(data)
                        }
                    });

                    getRef.fail(function( jqXHR, textStatus, errorThrown ) {
                        alert( 'Error: ' + textStatus + errorThrown )
                    });
                }
             });

            shortener.fail(function( jqXHR, textStatus, errorThrown ) {
                alert( 'Error: ' + textStatus + errorThrown )
            });
            
            event.preventDefault();
        });
        
        var refChecked = [];

        $('#references .delbtn').click(function (){
            $('input[type=checkbox]').each(function () {
                if (this.checked)
                    refChecked.push(parseInt($(this).val()));
            });
            
            var refData = $.ajax({
              method: 'POST',
              data: "{" + "'action' : " + 0
                     + ", 'refsID' : " + "[" + refChecked + "]" + "}",
              dataType: 'text',
              success: function (data) {
                    location.reload();
                }
            });
            
            refData.fail(function( jqXHR, textStatus, errorThrown ) {
            alert( 'Error: ' + textStatus + errorThrown )
            }); 
        });
    });
};

/*
 * Timer page, using easytimer
 */
function chrono() {
    $(document).ready(function () {
        var timer = new Timer();                                                        //instantiate timer
        
        $('#easyTimer .startButton').click(function () {                                // timer buttons
            timer.start({startValues: {minutes: 42}});
        });
        $('#easyTimer .pauseButton').click(function () {
            timer.pause();
        });
        
        $('#easyTimer .stopButton').click(function () {                                 // POST values as minutes when stop is clicked
            var getTime = $.ajax({
              method: 'POST',
              data: "{" + "'taskID' : " + parseInt($('#currentTaskID').html())
                     + ", 'minutes' : " + timer.getTotalTimeValues().minutes + "}",
              dataType: 'text',
              success: function (data) {
                    timer.stop();
                    window.location = "/";
                }
            });

            getTime.fail(function( jqXHR, textStatus, errorThrown ) {
            alert( 'Error: ' + textStatus + errorThrown )
            });

        });
        
        timer.addEventListener('secondsUpdated', function (e) {                         // update display for every second
            $('#easyTimer .hours').html(timer.getTimeValues().hours);
            $('#easyTimer .minutes').html(timer.getTimeValues().minutes);
            $('#easyTimer .seconds').html(timer.getTimeValues().seconds);
        });
        timer.addEventListener('started', function (e) {                                // update display when start is clicked
            $('#easyTimer .hours').html(timer.getTimeValues().hours);
            $('#easyTimer .minutes').html(timer.getTimeValues().minutes);
            $('#easyTimer .seconds').html(timer.getTimeValues().seconds);
        });
        


    });   
};

/*
 * Format input as text for objective
 */ 
function str_time(hour, minute){

    if (minute == 0)
        return hour + ' : 00';
        
    if ((minute >= 0) && (minute <= 9))
        return hour + ' : ' + '0' + minute;

    return hour + ' : ' + minute;
};
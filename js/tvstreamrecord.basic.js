/*
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.

    @author: pavion
    @version: v0.4.1
*/

var dialognr = -1; 

function checkLength( o, n, min, max ) {
    x = document.getElementById(o);
    if ( x.value.length > max || x.value.length < min ) {
        $("#"+o).addClass( "ui-state-error" );
        updateTips( "Length of " + n + " must be between " +
        min + " and " + max + "." );
        return false;
    } else {
        return true;
    }
}

function checkRegexp( o, regexp, n ) {
    x = document.getElementById(o);
    if ( !( regexp.test( x.value ) ) ) {
        $("#"+o).addClass( "ui-state-error" );
        updateTips( n );
        return false;
    } else {
        return true;
    }
}

function initProgressbar() {
	$( "[id^=progressbar]" ).each(function(i) {
        $(this).progressbar({
            value: parseInt($(this).attr('id').replace("progressbar","")),
        });
        $(this).width(100);
        $(this).height(14);
        $(this).css("float", "left");
    });
}
 
function initIcons() {
	$( "[id^=icons-]" ).hover(
		function() {
			$( this ).addClass( "ui-state-hover" );
		},
		function() {
			$( this ).removeClass( "ui-state-hover" );
		}
	);

	$( "[id^=icons-]" ).click(function( event ) {
        dialognr = parseInt($(this).attr('id').replace("icons-",""));
		$( "#dialog" ).dialog( "open" );
		event.preventDefault();            
	});
	
	$( "[id^=icons-]" ).each(function(i) {
        $(this).height(14);
        $(this).width(14);
        $(this).css("margin-left", "7px");
    });
}


function initSwitch() {
    $('[id^=switch-]').each(function() {
    	//$(this).css("margin-top", "2px"); 
        var switchnr = parseInt($(this).attr('id').replace("switch-",""));
        var postto = window.location.href.slice(window.location.href.lastIndexOf("/"));
        $(this).slickswitch({
            toggledOn: function() {            
                post(postto, { myid:switchnr, what:"1" }, 0); 
            },
            toggledOff: function() {  
                post(postto, { myid:switchnr, what:"0" }, 0); 
            }
        });
    });
}

function post(dest1, data1, rel) {
    $.ajax({
        type: "POST",
        url: dest1,
        data: data1,
        dataType: "json",
        success: function(data, textStatus) {
            if(rel==1) { 
                window.location.reload(false);                            
            }
        }
    });                        
}

function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

$(function() {
	
    var pickerform = "dd.mm.yy";

	$( "#accordion" ).accordion();
	
	var availableTags = [
		"ActionScript",
		"AppleScript",
		"Asp",
		"BASIC",
		"C",
		"C++",
		"Clojure",
		"COBOL",
		"ColdFusion",
		"Erlang",
		"Fortran",
		"Groovy",
		"Haskell",
		"Java",
		"JavaScript",
		"Lisp",
		"Perl",
		"PHP",
		"Python",
		"Ruby",
		"Scala",
		"Scheme"
	];
	$( "#autocomplete" ).autocomplete({
		source: availableTags
	});
		

		
	//$( "#button" ).button();
	$( "#radioset" ).buttonset();
	

    $("#timepicker_inline_div1").timepicker({
        constrainInput: true,
        showPeriodLabels: false
    });
    $("#timepicker_inline_div2").timepicker({
        constrainInput: true,
        showPeriodLabels: false
    });
    
    $( "#switch00" ).slickswitch();   
    $( "#switch01" ).slickswitch();
    
	$( "#dialog" ).dialog({
		autoOpen: false,
		width: 300,
		buttons: [
			{
				text: "Delete",
				click: function() {
                    var postto = window.location.href.slice(window.location.href.lastIndexOf("/"));
                    post(postto, { myid:dialognr, what:"-1" }, 1);
					$( this ).dialog( "close" );                        
				}
			},
			{
				text: "Cancel",
				click: function() {
					$( this ).dialog( "close" );
				}
			}
		]
	});

	$( "#confirm01" ).dialog({
		autoOpen: false,
		width: 300,
		buttons: [
			{
				text: "OK",
				click: function() {
                    var postto = window.location.href.slice(window.location.href.lastIndexOf("/"));
                    post(postto, { myid:'-1', what:"-2" }, 1);
					$( this ).dialog( "close" );                        
				}
			},
			{
				text: "Cancel",
				click: function() {
					$( this ).dialog( "close" );
				}
			}
		]
	});


	$( "#datepicker" ).datepicker({
        constrainInput: true,
        minDate: -1,          
        defaultDate: 0,        
        dateFormat: pickerform
	});

	$( "#datepicker3" ).datepicker({
        constrainInput: true,
        minDate: -1,          
        defaultDate: 0,
        onSelect: function() {
            document.daychooser.submit();
        },
        dateFormat: pickerform
	});

	
	$( "#slider" ).slider({
		range: true,
		values: [ 17, 67 ]
	});
	

    var selcount = 0;
    $( "#selectabletitle" ).selectable({
        disabled: true,
        autoRefresh: false
    });
    $( "#selectable" ).selectable({ distance: 99999 } );
   
    $(function() {
        $( document ).tooltip();
    });
	
	$( "[id=event]" ).each(function(i) {        
		w = $(this).attr('width')+"%";
		x = $(this).attr('x')+"%";
        $(this).css("margin-left", x);		
        $(this).css("width", w);		
	});
	
    $("[id^=wwd]").each(function() { 
    	$(this).live("click", function(event) {
    	/*	if ($(this).hasClass("ui-state-active")) {
    			$(this).removeClass("ui-state-active");
    			$(this).css("background", "#accccc");    			
    			    			//console.log("test");
    		} else {
    			$(this).addClass("ui-state-active");
    			$(this).css("background", "#e6e6e6");    			
    			
    		}*/
//    		console.log( $("#wwd0").attr("aria-pressed")  );
    	});
    });

    $("li").live("click", function(event) {
   		$("li").siblings().removeClass("ui-selected");        
   		$(this).addClass("ui-selected");
   		var ft = $(this).attr("fulltext");
   		//console.log (ft);
   		if (ft)   {
			document.getElementById("ret").value = $(this).attr("rid");             
			$("#dialog_content").html ( ft );	
	        $( "#record_from_epg" ).dialog( "open" );
   		}
        
	});

	
    var allFields =  $( [] ).add( "#recname" ).add( "#channel" ).add( "#datepicker" ).add( "#timepicker_inline_div1" ).add( "#timepicker_inline_div2" );
    function updateTips( t ) {
        $( ".validateTips" )
        .text( t )
        .addClass( "ui-state-highlight" );
        setTimeout(function() {
            $( ".validateTips" ).removeClass( "ui-state-highlight", 1500 );
        }, 500 );
    }
    $( "#dialog-form" ).dialog({
        autoOpen: false,
        height: 350,
        width: 350,
        modal: true,
        buttons: {
            "Schedule a record": function() {
                var bValid = true;
                allFields.removeClass( "ui-state-error" );
                bValid = bValid && checkLength( "recname", "record name", 1, 20 );
                bValid = bValid && checkRegexp( "recname", /^(?!^(PRN|AUX|CLOCK\$|NUL|CON|COM\d|LPT\d|\..*)(\..+)?$)[^\x00-\x1f\\?*:\";|//]+$/, "No special chars in this field please" );
                bValid = bValid && checkLength( "channel", "channel", 1, 50 );
                bValid = bValid && checkLength( "datepicker", "date", 10, 10 );
                bValid = bValid && checkRegexp( "datepicker", /^((((0?[1-9]|[12]\d|3[01])[\.\-\/](0?[13578]|1[02])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|[12]\d|30)[\.\-\/](0?[13456789]|1[012])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|1\d|2[0-8])[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|(29[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00)))|(((0[1-9]|[12]\d|3[01])(0[13578]|1[02])((1[6-9]|[2-9]\d)?\d{2}))|((0[1-9]|[12]\d|30)(0[13456789]|1[012])((1[6-9]|[2-9]\d)?\d{2}))|((0[1-9]|1\d|2[0-8])02((1[6-9]|[2-9]\d)?\d{2}))|(2902((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00))))$/, "Please use DD.MM.YYYY for this field" );
                bValid = bValid && checkLength( "timepicker_inline_div1", "start time", 5, 5 );
                bValid = bValid && checkRegexp( "timepicker_inline_div1", /^(([0-1]?[0-9])|([2][0-3])):([0-5]?[0-9])(:([0-5]?[0-9]))?$/, "Please use HH:MM format for this field" );
                bValid = bValid && checkLength( "timepicker_inline_div2", "end time", 5, 5 );
                bValid = bValid && checkRegexp( "timepicker_inline_div2", /^(([0-1]?[0-9])|([2][0-3])):([0-5]?[0-9])(:([0-5]?[0-9]))?$/, "Please use HH:MM format for this field" );
                var mask = 0;
                for (var i=0; i<7; i++) {
                	if ( $("#wwd" + i).hasClass("ui-state-active") ) {
                		mask += Math.pow(2, i);
                	} 
                }
                //console.log(mask);
                if ( bValid ) {
                    $( this ).dialog( "close" );                    
                    var akt = 0;
                    if ($("#switch00").attr("checked") == "checked") {akt = 1;}
                    //alert (document.getElementById("timepicker_inline_div1").value);                    
                    post("/create", { 
                        recname:document.getElementById("recname").value, 
                        Sender:document.getElementById("channel").value, 
                        von:document.getElementById("timepicker_inline_div1").value, 
                        bis:document.getElementById("timepicker_inline_div2").value, 
                        am:document.getElementById("datepicker").value, 
                        aktiv:akt,
                        recurr:mask//document.getElementById("recurrinp").value
                    }, 1); 
                }
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        },
        close: function() {
            allFields.removeClass( "ui-state-error" ); //.val( "" )
        }
    });

    $( "#record_from_epg" ).dialog({
        autoOpen: false,
        height: 310,
        width: 350,
        modal: true,
        buttons: {
            "Record": function() {
                $( this ).dialog( "close" );
				$("#dialog_content").html("");
	            document.returnform.submit();	            
            },
            Cancel: function() {
                $( this ).dialog( "close" );
				$("#dialog_content").html("");
            }
        },
        close: function() {
			$("#dialog_content").html("");
        }
    });


    
    $( "#upload-form" ).dialog({
        autoOpen: false,
        height: 190,
        width: 270,
        modal: true,
        buttons: {
            "Upload file": function() {
                $( this ).dialog( "close" );                    
                document.uploader.submit();                
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        },
        close: function() {
            allFields.val( "" ).removeClass( "ui-state-error" );
        }
    });
    
    $( "#createchannel-form" ).dialog({
        autoOpen: false,
        height: 195,
        width: 250,
        modal: true,
        buttons: {
            "Create channel": function() {
                $( this ).dialog( "close" );    
                var akt = 0;
                if ($("#switch01").attr("checked") == "checked") {akt = 1;}
                post("/create_channel", { 
                    cname:document.getElementById("cname").value, 
                    cpath:document.getElementById("cpath").value, 
                    aktiv:akt 
                }, 1);                                 
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        },
        close: function() {
            allFields.val( "" ).removeClass( "ui-state-error" );
        }
    });

    $( "#create-user" )
        .button()
        .click(function() {
            $( "#dialog-form" ).dialog( "open" );
        });

    $( "#purge-records" )
        .button()
        .click(function() {
            $( "#confirm01" ).dialog( "open" );
        });

        
    $( "#getepg" )
        .button()
        .click(function(event ) {
            post("/getepg", {}, 0);                  
            event.preventDefault();
        });

    $( "#resetlog" )
        .button()
        .click(function(event ) {
            post("/resetlog", {}, 1);                  
            event.preventDefault();
        });

    $( "#create-channel" )
        .button()
        .click(function(event ) {
            $( "#createchannel-form" ).dialog( "open" );
            event.preventDefault();
        });
        
    $( "#upload-user" )
        .button()
        .click(function(event ) {
            $( "#upload-form" ).dialog( "open" );
            event.preventDefault();
        });

    $( "#submit_cfg" )
        .button()
        .click(function(event ) {
            document.submit_cfg_form.submit();
            event.preventDefault();
        });
        
    $( "#downlog" )
        .button()
        .click(function(event ) {
            window.location = "./log.txt";
            event.preventDefault();
        });
       

 	$( "#wday" ).button();
	$( "#weekday" ).buttonset();
  
 	$('#clist').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "sAjaxSource": "/channellist",
        "fnDrawCallback": function( oSettings ) {
            initSwitch();
            initIcons();
            
        },
        "fnRowCallback": function( nRow, aData, iDisplayIndex ) {        
            var chk = "";
            if (aData[3] == 1) chk = 'checked="checked"';
            $('td:eq(3)', nRow).html('<input type="checkbox" class="switch icons" id="switch-' + aData[0] + '" ' + chk + ' /><a href="#" id="icons-' + aData[0] + '" class="ui-state-default ui-corner-all"><span class="ui-icon ui-icon-trash"></span></a>');            
        }        
    }); 
    
 	$('#recordlist').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "sAjaxSource": "/getrecordlist",
        "aoColumnDefs": [ { "bSearchable": false, "bVisible": false, "aTargets": [ 6,7,8,9 ] },
        				  { "iDataSort": 8, "aTargets": [ 2 ] }, 
        				  { "iDataSort": 9, "aTargets": [ 3 ] } ],
        "fnDrawCallback": function( oSettings ) {
            initSwitch();
            initIcons();
            initProgressbar();
            
        },
        "fnRowCallback": function( nRow, aData, iDisplayIndex ) {        
            var chk = "";
            if (aData[5] == 1) chk = 'checked="checked"';
            htmltext  = '<div id="progressbar' + aData[6] + '"></div>';
            htmltext += '<input type="checkbox" class="switch icons" id="switch-' + aData[7] + '" ' + chk + ' />';  
			htmltext += '<a href="#" id="icons-' + aData[7] + '" class="ui-state-default ui-corner-all"><span class="ui-icon ui-icon-trash"></span></a>';                        
            $('td:eq(5)', nRow).html(htmltext);            
        },
        "fnInitComplete": function() {
		 	this.fnSort([ [2,'desc'] ]);        	
        } 
        
    }); 

 	$('#loglist').dataTable({
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bProcessing": true,
        "sAjaxSource": "/logget",
        "fnInitComplete": function() {
		 	this.fnSort([ [0,'desc'] ]);        	
        } 
    }); 
    
    $(window).bind('resize', function () {
    	$('#loglist').dataTable().fnAdjustColumnSizing();
    	$('#recordlist').dataTable().fnAdjustColumnSizing();
    	$('#clist').dataTable().fnAdjustColumnSizing();
  	} );
    
            
});
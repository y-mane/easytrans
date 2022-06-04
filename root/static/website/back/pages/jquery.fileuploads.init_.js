
/**
* Theme: Zircos Admin Template
* Author: Coderthemes
 * Email: coderthemes@gmail.com
* File Uploads
*/

$(document).ready(function(){

	'use-strict';

    //Example 2
    $('#filer_input2').filer({
        limit: 3,
        maxSize: 3,
        extensions: ['jpg', 'jpeg', 'png', 'gif', 'psd'],
        changeInput: true,
        showThumbs: true,
        addMore: true
    });

	//Example 1
    $("#filer_input1").filer({
        limit: 1,
        maxSize: 3,
        extensions: ['xls', 'xlsx', 'csv'],
        showThumbs: true,
        theme: "dragdropbox",
        dragDrop: {
            dragEnter: null,
            dragLeave: null,
            drop: null,
        },
        addMore: false,
        clipBoardPaste: true,
        excludeName: null,
        beforeRender: null,
        afterRender: null,
        beforeShow: null,
        beforeSelect: null,
        onSelect: null,
        afterShow: null,
        onEmpty: null,
        options: null,
        captions: {
            button: "Choose Files",
            feedback: "Choose files To Upload",
            feedback2: "files were chosen",
            drop: "Drop file here to Upload",
            removeConfirmation: "Are you sure you want to remove this file?",
            errors: {
                filesLimit: "Only {{fi-limit}} files are allowed to be uploaded.",
                filesType: "Seulement les Fichiers Excel sont autorisés.",
                filesSize: "{{fi-name}} is too large! Please upload file up to {{fi-maxSize}} MB.",
                filesSizeAll: "Files you've choosed are too large! Please upload files up to {{fi-maxSize}} MB."
            }
        }
    });
});

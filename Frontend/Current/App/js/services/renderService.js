angular.module("mixTapeApp")
.factory("renderService", ["globalSettings", "scoreService",
function(globalSettings, scoreService) {
    "use strict";

    return {
        clearStaff: function(staff){
            var staffElem = $("#" + staff)[0];
            var rows = staffElem.children
            for(var i = 0; i < rows.length; i++){
                var row = rows[i];
                var cols = row.children;
                for(var j = 0; j < cols.length; j++){
                    this.clearNote(cols[j],i);
                }
            }
        },

        clearNote: function(col, i){
            if (i % 2 == 0 && i >= globalSettings.TOP_LINE_INDEX && i < globalSettings.trebleStaff.length - 1){
                if(col.children.length >= 2){
                    for (var k = 1; k < col.children.length; k++){
                        col.removeChild(col.children[k]);
                    }
                }
            }
            else{
                if(col.children.length >= 1){
                    for (var k = 0; k < col.children.length; k++){
                        col.removeChild(col.children[k]);
                    }
                }
            }
        },

        generateStaff: function(id){
            var idString = ' id="'+id+'" '
            var idVar = "this." + id + "Staff";
            var staff = '<div '+idString+' class="staff">';
            var noteWidthPercentage = (globalSettings.NOTE_RADIUS*2)*100;
            var notePercentage = (globalSettings.LINE_HEIGHT/2) *100;
            var curLines = 0;

            for (var i = 0; i < globalSettings.trebleStaff.length; i++){
                var line = "";

                if (i % 2 == 0 && i >= globalSettings.TOP_LINE_INDEX
                    && curLines < globalSettings.STAFF_LINES){

                        line = '<line x1="0%" y1="50%" x2="100%" y2="50%" style="stroke:rgb(0,0,0);stroke-width:2"/>';
                        curLines += 1;
                    }

                    staff += '<div id="'+String(i)+'" class="row" style="height:' + String(notePercentage)+'%;">';
                    for (var j = 0; j < 1/(globalSettings.NOTE_RADIUS*2); j++){
                        staff += '<svg id="'+String(j)+'" style="width:' + noteWidthPercentage + '%;"ng-click="drawNote('+i+','+j+','+idVar+')" class="cell"'+
                        '>' + line + '</svg>';

                    }
                    staff += '</div>';
                }
                staff += '</div>';
                return staff
        },

        generateNoteHTML : function(noteType, pitchType){
            var namespace = "http://www.w3.org/2000/svg";
            var img = document.createElementNS(namespace, "image");
            var imgFile = "";

            if (noteType == globalSettings.noteType.WHOLE) {
                if (pitchType == globalSettings.pitchType.SHARP) {
                    imgFile = "App/img/whole_sharp.png";
                } else if (pitchType == globalSettings.pitchType.FLAT) {
                    imgFile = "App/img/whole_flat.png";
                } else {
                    imgFile = "App/img/whole.png";
                }
            }
            else if (noteType == globalSettings.noteType.HALF) {
                if (pitchType == globalSettings.pitchType.FLAT) {
                    imgFile = "App/img/half_flat.png";
                } else if (pitchType == globalSettings.pitchType.SHARP) {
                    imgFile = "App/img/half_sharp.png";
                } else {
                    imgFile = "App/img/half.png";
                }
            }
            else if (noteType == globalSettings.noteType.QUARTER) {
                if (pitchType == globalSettings.pitchType.FLAT) {
                    imgFile = "App/img/quarter_flat.png";
                } else if (pitchType == globalSettings.pitchType.SHARP) {
                    imgFile = "App/img/quarter_sharp.png";
                } else {
                    imgFile = "App/img/quarter.png";
                }
            }
            else if (noteType == globalSettings.noteType.EIGHTH) {
                if (pitchType == globalSettings.pitchType.FLAT) {
                    imgFile = "App/img/eighth_flat.png";
                } else if (pitchType == globalSettings.pitchType.SHARP) {
                    imgFile = "App/img/eighth_sharp.png";
                } else {
                    imgFile = "App/img/eighth.png";
                }
            }
            else if (noteType == globalSettings.noteType.SIXTEENTH) {
                if (pitchType == globalSettings.pitchType.FLAT) {
                    imgFile = "App/img/sixteenth_flat.png";
                } else if (pitchType == globalSettings.pitchType.SHARP) {
                    imgFile = "App/img/sixteenth_sharp.png";
                } else {
                    imgFile = "App/img/sixteenth.png";
                }
            }

            img.setAttributeNS(null, "href", imgFile);
            img.setAttributeNS(null, "height", "200%");
            img.setAttributeNS(null, "width", "100%");
            img.setAttributeNS(null, "y", "-120%");
            return img;
        },
        convertToNote : function(i, pitchType, noteType){
            var pitch = globalSettings.trebleStaff[i];
            var time_duration = 1;
            var pitchFileMod = "";
            if (noteType == globalSettings.noteType.SIXTEENTH){
                time_duration = .25;
            }
            if(noteType == globalSettings.noteType.EIGHTH){
                time_duration = .5;
            }
            if(noteType == globalSettings.noteType.HALF){
                time_duration = 2;
            }
            if(noteType == globalSettings.noteType.WHOLE){
                time_duration = 4;
            }
            if (pitchType == globalSettings.notePitchMod.SHARP){
                pitchFileMod = "#";
            }
            if(pitchType == globalSettings.notePitchMod.FLAT){
                pitchFileMod = "-";
            }
            var fileString = pitch.substr(0,1) + pitchFileMod + pitch.substr(1,1);
            var note = {"note":fileString, "duration":time_duration};
            return note;
        },

        resizeScore: function(width) {
            scoreService.resizeDisplay(window.innerWidth);
        },

        drawScore: function(melody, chord) {
            scoreService.drawScore(melody, chord);
        },

        initialise: function(melodyScore, chordsScore) {
            scoreService.initialise(melodyScore, chordsScore);
        }
    }
}]);

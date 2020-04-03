function play_video(vid){
    var myPlayer = videojs.getPlayer('my-player');

    if (vid['vid_width'] > 2000){
        myPlayer.width(2000);
    }else{
        myPlayer.width(vid['vid_width'])
    }
    myPlayer.src({type: 'video/mp4', src: 'http://127.0.0.1:8888/stuff'+vid['vid_web_path']});
    display_video_info();
}

function display_video_info(){
    var vid = playlist[playlist_index];
    var duration_in_seconds = vid['vid_duration_in_seconds']; //TODO: Handle videos where the seconds are undefined.  ddd56a899b67e469e0c6caa2169a3371
    var seconds = duration_in_seconds % 60;
    var minutes = (duration_in_seconds - seconds) / 60;
    var vid_top_summary_text = `${vid['vid_width']}x${vid['vid_height']} ${minutes}m${seconds}s  MD5:${vid['vid_md5']} <br> ${vid['vid_web_path']}`;
    var playlist_info_display = `<h3>Playlist Position ${playlist_index+1} of ${playlist.length}</h3>`;

    $('#vid_top_summary').html(`${vid_top_summary_text}`);
    $('#playlist_info').html(`${playlist_info_display}`);

    var vid_tags;
    axios.get('http://localhost:8000/tag/'+vid['vid_md5'])
        .then(function (response) {
            vid_tags = response.data;
            create_buttons_for_tags(vid_tags);
        })
        .catch(function (error) {
            console.log("Issue grabbing tags: " + error);
        })
}

function play_next_video() {
    if (playlist_index+1 < playlist.length){
        playlist_index += 1;
    } else{
        playlist_index = 0;
    }
    play_video(playlist[playlist_index])
}

function play_previous_video() {
    if (playlist_index <= 0){
        playlist_index = playlist.length - 1; // Set to last item in the list.
    } else {
        playlist_index -= 1;
    }
    play_video(playlist[playlist_index])
}

function move_playhead(seconds){
    var myPlayer = videojs.getPlayer('my-player');
    myPlayer.currentTime(myPlayer.currentTime() + seconds);
}

function update_playlist(){
    axios.get('http://localhost:8000/video_playlist')
        .then(function (response) {
            playlist = response.data;
            play_video(playlist[0])
        })
        .catch(function (error) {
            console.log("Issue Updating the playlist: " + error);
        })
    ;
}

function update_playlist_with_tag(tag) {
    // Strip off the (COUNT) from end of the tag
    let re_1 = " \\(.*$";
    let offset = tag.search(re_1);
    var tag_name;
    if (offset >=0){
        tag_name = tag.substring(0, offset);
    } else {
        tag_name = tag;
    }


    axios.get('http://localhost:8000/video_playlist/'+tag_name)
        .then(function (response) {
            playlist = response.data;
            console.log("Updating to use " + playlist.length + " videos with tag: " + tag_name);
            play_video(playlist[0]);
        })
        .catch(function (error) {
            console.log("Issue Updating the playlist with tag: " + error);
        })
    ;
}

function create_buttons_for_tags(tags){
    // Remove existing buttons
    $("#tag_buttons_here").empty();

    // Create buttons for tags
    for(let i=0; i < tags.length; i++){
        let tag_name = tags[i]['tag_name'];
        let tag_count = tags[i]['tag_count'];
        $(`<button class="badge badge-secondary mr-1 " type="button">${tag_name} (${tag_count})</button>`).on('click', function () {
            console.log("Clicked on " + $(this).text() );
            update_playlist_with_tag($(this).text());
        }).appendTo( "#tag_buttons_here" );
    }

    // Update tags_for_current_video
    tags_for_current_video = [];
    for(let i=0; i < tags.length; i++){
        let tag_name = tags[i]['tag_name'];
        tags_for_current_video.push(tag_name);
    }

}

function configure_keyboard_shortcuts(){
    // Keyboard shortcuts

    // Previous Video
    Mousetrap.bind('alt+left', function() {
        play_previous_video()
    }, 'keyup');

    // Next Video
    Mousetrap.bind('alt+right', function() {
        play_next_video()
    }, 'keyup');

    // Forward 10 seconds
    Mousetrap.bind('shift+down', function() {
        move_playhead(10)
    }, 'keyup');

    // Backward 10 seconds
    Mousetrap.bind('shift+up', function() {
        move_playhead(-10)
    }, 'keyup');

    // Forward 30 seconds
    Mousetrap.bind('right', function() {
        move_playhead(30);
    }, 'keyup');

    // Backward 30 seconds
    Mousetrap.bind('left', function() {
        move_playhead(-30);
    }, 'keyup');

    // Forward 60 seconds
    Mousetrap.bind('shift+right', function() {
        move_playhead(60);
    }, 'keyup');

    // Backward 60 seconds
    Mousetrap.bind('shift+left', function() {
        move_playhead(-60);
    }, 'keyup');

    // Toggle Favorite
    Mousetrap.bind('f', function() {
        toggle_favorite();
    }, 'keyup');

    // Mark Won't Play
    Mousetrap.bind('w', function() {
        flag_current_video_wont_play();
    }, 'keyup');

    // Delete Video
    Mousetrap.bind('d', function() {
        delete_current_video();
    }, 'keyup');

    // Modify Video Tags
    Mousetrap.bind('m', function() {
        set_current_video_tags_in_modify_tag();
        $("#modifyTagModalCenter").modal("show");
    }, 'keyup');

}

function toggle_favorite() {
    var vid = playlist[playlist_index];
    var is_already_fav = false;
    var new_tags_list = [];

    // move all tags to a new list unless tag is favs.
    for(let i=0; i < tags_for_current_video.length; i++){
        let tag_name = tags_for_current_video[i];
        if (tag_name === "favs"){
            is_already_fav = true;
        }
        if (tag_name !== "favs"){
            new_tags_list.push(tag_name);
        }
    }

    // add favs if we didn't find the favs tag.
    if (!is_already_fav){
        new_tags_list.push("favs");
        console.log("Toggle favorite to On.");
    } else {
        console.log("Toggle favorite to Off.");
    }

    // Update tags
    axios.post('http://localhost:8000/tag', {
        'vid_md5': vid['vid_md5'],
        'tag_names': new_tags_list
    })
        .then(function (response) {
            console.log("Tags Updated" + response);
            console.log("Reloading Video");
            play_video(playlist[playlist_index]);
        })
        .catch(function (error) {
            console.log("There was an issue adding a tag" + error);
        })
}

function flag_current_video_wont_play() {
    var vid_md5 = playlist[playlist_index]['vid_md5'];

    axios.delete('http://localhost:8000/flag_as_wont_play/'+vid_md5)
        .then(function (response) {
            console.log("Video moved to Won't Play folder" + response);
            play_next_video();
        })
        .catch(function (error) {
            console.log("There was an issue moving the video to won't play folder" + error);
        })
}

function delete_current_video() {
    var vid_md5 = playlist[playlist_index]['vid_md5'];

    axios.delete('http://localhost:8000/video/'+vid_md5)
        .then(function (response) {
            console.log("Video Deleted" + response);
            play_next_video();
        })
        .catch(function (error) {
            console.log("There was an issue deleting the video" + error);
        })
}

function modify_video_tags() {
    var vid_md5 = playlist[playlist_index]['vid_md5'];
    var tags_from_selectize = selectize_modify_tags[0].options;
    var tags_list = [];

    for(let i=0; i < tags_from_selectize.length; i++){
        let tag_text = tags_from_selectize[i].text;
        tags_list.push(tag_text);
    };

    axios.post('http://localhost:8000/tag', {
        'vid_md5': vid_md5,
        'tag_names': tags_list
    })
        .then(function (response) {
            console.log("Tags Updated" + response);
            console.log("reloading Video");
            play_video(playlist[playlist_index]);
        })
        .catch(function (error) {
            console.log("There was an issue adding a tag" + error);
        })
}

function set_current_video_tags_in_modify_tag(){
    var select = $('#modify-tags-select').selectize();
    var control = select[0].selectize;
    control.clear();
    control.addItems(tags_for_current_video);
}

function init_modify_tags_select(){
    axios.get('http://localhost:8000/tag')
        .then(function (response) {
            var list_of_tags_name_only = response.data;

            var list_of_tags_dict_for_selectize = [];

            for(let i=0; i < list_of_tags_name_only.length; i++){
                let option_value = list_of_tags_name_only[i];
                let option_text = list_of_tags_name_only[i];
                list_of_tags_dict_for_selectize.push({'value': option_value, 'text': option_text})
            };

            a=1;

            selectize_modify_tags = $('#modify-tags-select').selectize({
                maxItems: 20,
                maxOptions: 1000,  //this is 1000 by default.  May need to increase this if we add more than 1000 tags
                required: false,
                options: list_of_tags_dict_for_selectize,//[{value:"val1", text: "item1"}],
                hideSelected: true,
                openOnFocus: false,
                allowEmptyOption: true,
                closeAfterSelect: true,
                placeholder: "tags here",
                autocomplete: "on",
                create: true,  //Add ability to create items not in the list.  This can be a function. TODO: add a function to write the new tag to the database
                onInitialize: function (value) {
                    a = 1; //Just a placeholder
                },
                onChange: function(value){
                    console.log("Value is: "+ value);
                    // add_tag_to_video(playlist[playlist_index], value)
                    // update_playlist_with_tags(value);
                }
            });
        })
        .catch(function (error) {
            console.log("Issue grabbing tags (names only): " + error);
        });
}

function init_filter_by_tag(){
    axios.get('http://localhost:8000/tag')
        .then(function (response) {
            var list_of_tags_name_only = response.data;

            var list_of_tags_dict_for_selectize = [];

            for(let i=0; i < list_of_tags_name_only.length; i++){
                let option_value = list_of_tags_name_only[i];
                let option_text = list_of_tags_name_only[i];
                list_of_tags_dict_for_selectize.push({'value': option_value, 'text': option_text})
            };

            a=1;

            selectize_tag_filter = $('#filter-by-tag-select').selectize({
                maxItems: 1,
                maxOptions: 1000,  //this is 1000 by default.  May need to increase this if we add more than 1000 tags
                required: false,
                options: list_of_tags_dict_for_selectize,//[{value:"val1", text: "item1"}],
                hideSelected: true,
                openOnFocus: false,
                allowEmptyOption: true,
                closeAfterSelect: true,
                placeholder: "Filter by tag",
                autocomplete: "on",
                create: true,  //Add ability to create items not in the list.  This can be a function. TODO: add a function to write the new tag to the database
                onInitialize: function (value) {
                    a = 1; //Just a placeholder
                },
                onChange: function(value){
                    console.log("Value is: "+ value);
                    update_playlist_with_tag(value);
                    // update_playlist_with_tags(value);
                }
            });
        })
        .catch(function (error) {
            console.log("Issue grabbing tags (names only): " + error);
        });
}

$('document').ready(function(){

    configure_keyboard_shortcuts();

    update_playlist();

    init_filter_by_tag();
    init_modify_tags_select();

    // ensure modal gets focus
    $('#modifyTagModalCenter').on('shown.bs.modal', function () {
        $('#modify-tags-select-selectized').trigger('focus')
    })

});

var playlist_index = 0;
var playlist;
var tags_for_current_video = [];













//
//
// function send_vid_wontplay(vid_json) {
//     console.log("Video Won't play - button clicked");
//     var md5_string = current_video.md5;
//
//     $.ajax({
//         url: "/video_wontplay",
//         type: "get",
//         data: {jsdata: md5_string},
//         success: function (response) {
//             console.log("won't play video sent");
//             grab_next_video();
//         },
//         error: function (xhr) {
//             console.log("won't video did not send - Something went wrong");
//         }
//     });
// }
//
// function send_vid_delete() {
//     console.log("Delete Video Button Clicked");
//     var md5_string = current_video.md5;
//
//     $.ajax({
//         url: "/video_delete",
//         type: "get",
//         data: {jsdata: md5_string},
//         success: function (response) {
//             console.log("delete video sent");
//             grab_next_video();
//         },
//         error: function (xhr) {
//             console.log("delete video did not send - Something went wrong");
//         }
//     });
//
// }
//
// function toggle_favorite() {
//     console.log("Toggle Favorite Video Button Clicked");
//     var md5_string = current_video.md5;
//
//     $.ajax({
//         url: "/video_toggle_favorite",
//         type: "get",
//         data: {jsdata: md5_string},
//         success: function (response) {
//             console.log("Toggle Favorite video sent");
//         },
//         error: function (xhr) {
//             console.log("Toggle Favorite video did not send - Something went wrong");
//         }
//     });
//
// }
//


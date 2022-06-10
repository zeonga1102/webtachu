function click_modify_button(text, book_id, review_id) {
    document.getElementById('modify_desc').value = text
    document.getElementById('modify_modal_inner').setAttribute('action', `/book/${book_id}/review/modify/${review_id}`)
}
function(doc, meta) {
    if(doc.doc_type && doc.doc_type == "flashcards" && doc.taskgroup) {
        emit(meta.id)
    }
}
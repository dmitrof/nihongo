function (doc, meta) {
    if (!doc.st_deleted && doc.doc_type == 'article') {
        emit(doc.author_uid, 1);
    }
}
/**
 * IndexedDB sample.
 */

$(function() {
    var $log = $('#idb-log');

    // Install action handler for user-interface.
    $('form[action="#set"]').submit(function(event) {
        event.preventDefault();
        var $key = $('input[name=key]', this),
            $val = $('input[name=val]', this);
        if (!$key.val() || !$val.val()) {
            $log.text("Input key and value.");
            $log.addClass('error');
            setTimeout(function() { $log.removeClass('error'); }, 5000);
            return;
        }
        indexedDbUtil.idbSet($key.val(), $val.val());
        $key.val('').blur();
        $val.val('').blur();
    });

    $('#idb-remove').hide();
    $('#idb-create').click(function(e) {
        indexedDbUtil.idbCreate();
        $(this).toggle();
        $('#idb-remove').toggle();
    });
    $('#idb-remove').click(function(e) {
        indexedDbUtil.idbRemove();
        $(this).toggle();
        $('#idb-create').toggle();
    });
    $('.idb-key').live('blur', function(e) {
        var key = $(this).data('key'),
            newKey = $(this).text();
        if (!newKey) {
            $log.text("Empty key is prohibited.");
            $log.addClass('error');
            setTimeout(function() { $log.removeClass('error'); }, 5000);
            $(this).text(key);
            return;
        }
        indexedDbUtil.updateKey(key, newKey);
    });
    $('.idb-value').live('blur', function(e) {
        var key = $(this).data('key'),
            value = $(this).text();
        indexedDbUtil.updateValue(key, value);
    });
    $('.idb-delete').live('click', function(e) {
        var key = $(this).data('key');
        indexedDbUtil.deleteKey(key);
    });
});

var indexedDbUtil = (function() {
    var idb_;           // Our local DB
    var idbRequest_;    // Our DB request obj

    var STORAGE_NAME = 'myObjectStore';
    // just a simple way to show what we are doing on the page
    var $log = $('#idb-log'),
        $feedback = $('#idb-feedback'),
        $data = $('#idb-data');

    if ('webkitIndexedDB' in window) {
        window.indexedDB = window.webkitIndexedDB;
        window.IDBTransaction = window.webkitIDBTransaction;
    } else if ('mozIndexedDB' in window) {
        window.indexedDB = window.mozIndexedDB;
    }
    // Open our IndexedDB if the browser supports it.
    if (window.indexedDB) {
        idbRequest_ = window.indexedDB.open("Test", "Our Amazing test object IndexDB");
        idbRequest_.onerror = idbError_;
        idbRequest_.addEventListener('success', function(e) {
            // FF4 requires e.result. IDBRequest.request isn't set
            // FF5/Chrome works fine.
            idb_ = idbRequest_.result || e.result;
            showAll_(e);
        }, false);
    }

    function idbError_(e) {
        $log.text('Error: ' + e.message + ' (' + e.code + ')');
        $log.addClass('error');
        setTimeout(function() { $log.removeClass('error'); }, 5000);
    }

    // In cases we add/remove objects - show the user what is changing in the DB
    function idbShow_(e) {
        if (!idb_.objectStoreNames.contains(STORAGE_NAME)) {
            $log.text("Object store not yet created.");
            return;
        }
        var items = [];

        var key = e.currentTarget.result;
        var objectStore = idb_.transaction([], IDBTransaction.READ)
                            .objectStore(STORAGE_NAME),
            request = objectStore.get(key);
        request.onerror = idbError_;
        request.onsuccess = function(e) {
            var value = e.result || this.result;
            items.push({Key: key, Value: value});
            $('#idb-feedback-child').tmpl(items).appendTo($feedback);
            showAll_(e);
        }
    }

    // Simple example to show all our records in the DB
    // Enumerate the entire object store.
    function showAll_(e) {
        $data.empty();
        var transaction = idb_.transaction([], IDBTransaction.READ_ONLY),
            request = transaction.objectStore(STORAGE_NAME).openCursor();
        var items = [];
        // This callback will continue to be called until we have no more results.
        request.onsuccess = function(e) {
            var cursor = request.result || e.result;
            // If cursor is null then we've completed the enumeration.
            if (!cursor) {
                $('#idb-data-child').tmpl(items).appendTo($data);
                return;
            }
            items.push({Key: cursor.key, Value: cursor.value});
            cursor.continue();
        };
    }

    function idbCreate_() {
        if (!idb_) {
            if (idbRequest_) {
                // If indexedDB is still opening, just queue this up.
                idbRequest_.addEventListener('success', idb_.removeObjectStore, false);
            }
            return;
        }

        var request = idb_.setVersion('the new version string');
        request.onerror = idbError_;
        request.onsuccess = function(e) {
            if (!idb_.objectStoreNames.contains(STORAGE_NAME)) {
                try {
                    // FF is requiring the 2nd keyPath arg. It can be optional
                    var objectStore = idb_.createObjectStore(STORAGE_NAME, null);
                    $log.text("Object store created.");
                } catch (err) {
                    $log.text(err.toString());
                    $log.addClass('error');
                    setTimeout(function() { $log.removeClass('error'); }, 5000);
                }
            } else {
                $log.text('Object store already exists.');
            }
        }
    }

    function idbSet_(key, value) {
        if (!idb_) {
            if (idbRequest_) {
                // If indexedDB is still opening, just queue this up.
                idbRequest_.addEventListener('success', idb_.removeObjectStore, false);
            }
            return;
        }

        if (!idb_.objectStoreNames.contains(STORAGE_NAME)) {
            $log.text("Object store doesn't exist.");
            return;
        }
        // Create a transaction that locks the world.
        var objectStore = idb_.transaction([], IDBTransaction.READ_WRITE)
                                .objectStore(STORAGE_NAME),
            request = objectStore.put(value, key);
        request.onerror = idbError_;
        request.onsuccess = idbShow_;
    }

    function updateKey_(key, newKey) {
        // Create a transaction that locks the world.
        var transaction = idb_.transaction([], IDBTransaction.READ_WRITE),
            objectStore = transaction.objectStore(STORAGE_NAME),
            request = objectStore.get(key);
        request.onerror = idbError_;
        request.onsuccess = function(e) {
            // FF4 requires e.result. IDBRequest.request isn't set.
            // FF5/Chrome works fine.
            var value = e.result || this.result;
            if (objectStore.delete) {
                var request = objectStore.delete(key);
            } else {
                // FF4 not up to spect
                var request = objectStore.remove(key);
            }
            request.onerror = idbError_;
            request.onsuccess = function(e) {
                var request = objectStore.add(value, newKey);
                request.onerror = idbError_;
                request.onsuccess = idbShow_;
            };
        };
    }

    function updateValue_(key, value) {
        // Create a transaction that locks the world.
        var transaction = idb_.transaction([], IDBTransaction.READ_WRITE),
            objectStore = transaction.objectStore(STORAGE_NAME),
            request = objectStore.put(value, key);
        request.onerror = idbError_;
        request.onsuccess = idbShow_;
    }

    function deleteKey_(key) {
        // Create a transaction that locks the world.
        var transaction = idb_.transaction([], IDBTransaction.READ_WRITE),
            objectStore = transaction.objectStore(STORAGE_NAME);
        if (objectStore.delete) {
            var request = objectStore.delete(key);
        } else {
            // FF4 not up to spect
            // FF5 and Chrome - are by the book :)
            var request = objectStore.remove(key);
        }
        request.onerror = idbError_;
        request.onsuccess = idbShow_;
    }

    function idbRemove_() {
        if (!idb_) {
            if (idbRequest_) {
                // If indexedDB is still opening, just queue this up.
                idbRequest_.addEventListener('success', idb_.removeObjectStore, false);
            }
            return;
        }

        var request = idb_.setVersion("the new version string");
        request.onerror = idbError_;
        request.onsuccess = function(e) {
            if (idb_.objectStoreNames.contains(STORAGE_NAME)) {
                try {
                    // Spec has been updated to deleteObjectStore.
                    if (idb_.deleteObjectStore) {
                        idb_.deleteObjectStore(STORAGE_NAME);
                    } else {
                        idb_.removeObjectStore(STORAGE_NAME);
                    }
                    $feedback.empty();
                    $log.text("Object store removed.");
                } catch (err) {
                    $log.text(err.toString());
                    $log.addClass('error');
                    setTimeout(function() { $log.removeClass('error'); }, 5000);
                }
            } else {
                $log.text("Object store doesn't exist.");
                $log.addClass('error');
                setTimeout(function() { $log.removeClass('error'); }, 5000);
            }
        };
    }

    return {
        idbSet: idbSet_,
        idbCreate: idbCreate_,
        idbRemove: idbRemove_,
        updateKey: updateKey_,
        updateValue: updateValue_,
        deleteKey: deleteKey_,
        showAll: showAll_
    };
})();


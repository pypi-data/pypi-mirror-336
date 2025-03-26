window.onload = function () {
    jalaliDatepicker.startWatch(
        {
            separatorChars: {
                date: "-"
            },
            time: false,
            zIndex: 999999999,
            hasSecond: false,
            hideAfterChange: true,
        }
    );
}
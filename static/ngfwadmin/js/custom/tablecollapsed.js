   [].forEach.call(document.querySelectorAll('.toggler input'), function(input) {
  input.addEventListener('change', function() {

    var row = input.closest('tr');

    if (input.checked) {
      showChildRows(row);
    } else {
      hideChildRows(row);
    }
  })
});

//получить дочерние ряды всех уровней вложенности
function getChildRows(row) {
  var childRows = [],
    currentRow = row,
    startLevel = +row.getAttribute('data-level');

  while (currentRow && currentRow.nextElementSibling && +currentRow.nextElementSibling.getAttribute('data-level') > startLevel) {
    childRows.push(currentRow.nextElementSibling);
    currentRow = currentRow.nextElementSibling;
  }
  return childRows;
}

//скрыть все дочерние ряды
function hideChildRows(row) {
  var childRows = getChildRows(row);
  childRows.forEach(function(childRow) {
    childRow.classList.remove('dropdown--visible')
  })
}

//показать дочерние ряды в зависимости от состояния чекбокса
function showChildRows(row) {
  var childRows = getChildRows(row), //все дочерние ряды
    level = +row.getAttribute('data-level'),
    toggler = row.querySelector('.toggler input'),
    immediateChildren = childRows.filter(function(tr) {
      return tr.getAttribute('data-level') == level + 1
    }); //непосредственно дочерние ряды

  if (toggler && toggler.checked) { //если ряд раскрыт, показываем непосредственно дочерние ряды и повторяем для них такую же процедуру

    immediateChildren.forEach(function(childRow) {
      childRow.classList.add('dropdown--visible')
      showChildRows(childRow); //типа рекурсия
    })
  }
}

//кнопки
document.getElementById('slideUp').addEventListener('click', function() {
  [].forEach.call(document.querySelectorAll('.toggler input'), function(input) {
    input.checked = false
  });
  [].forEach.call(document.querySelectorAll('.dropdown--visible'), function(row) {
    row.classList.remove('dropdown--visible')
  });
})
document.getElementById('slideDown').addEventListener('click', function() {
  [].forEach.call(document.querySelectorAll('.toggler input'), function(input) {
    input.checked = true
  });
  [].forEach.call(document.querySelectorAll('.dropdown'), function(row) {
    row.classList.add('dropdown--visible')
  });
})
function makeBranchInteractive(branch) {
  $(branch).find('.addItem').click(function (e) {
    e.preventDefault();
    let $item = $('.prototype li.item').first().clone().removeClass('.prototype');
    makeItemInteractive($item);
    $(this).before($item);
  });
  let $items = $(branch).find('.item');
  _.forEach($items, makeItemInteractive);
}

function makeItemInteractive(item) {
  $(item).find('.addBranch').click(function (e) {
    e.preventDefault();
    let $li = $(this).parents('li.item').first();
    let $branch = $('.prototype').first().clone().removeClass('prototype');
    makeBranchInteractive($branch);
    $li.append($branch);
    $(this).addClass('hidden');
  });
  $(item).find('.delBranch').click(function (e) {
    e.preventDefault();
    let $li = $(this).parents('li.item').first();
    let $ul = $li.parent();
    console.log($ul.children('li'));
    $li.remove();
    if ($ul.children('li').length <= 1) {
      $ul.parents('li').find('.addBranch').removeClass('hidden');
      $ul.remove();
    }
  });
}

$(document).ready(function () {
  $('.branch').each((n, branch) => makeBranchInteractive(branch));
});
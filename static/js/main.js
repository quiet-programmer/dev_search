// script to make pagination work with search result

  let searchForm = document.getElementById('searchForm')
  let pageLink = document.getElementsByClassName('page-link')

  if(searchForm) {
    for(let index = 0; pageLink.length > index; index++) {
       pageLink[index].addEventListener('click', function (event) {
          event.preventDefault()

          let page = this.dataset.page

          searchForm.innerHTML += `<input value="${page}" name="page" type="hidden" />`

          searchForm.submit()
       })
    }
  }
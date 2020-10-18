async function onLike(event) {
    event.preventDefault();
    let likeBtn = event.target;
    let url = likeBtn.href;

    try {
        let response = await makeRequest(url, 'POST');
        let data = await response.text();
        console.log(data);
        const counter = likeBtn.parentElement.getElementsByClassName('counter')[0];
        counter.innerText = data;
    }
    catch (error) {
        console.log(error);
    }

    likeBtn.classList.add('hidden');
    const unlikeBtn = likeBtn.parentElement.getElementsByClassName('unlike')[0];
    unlikeBtn.classList.remove('hidden');
}
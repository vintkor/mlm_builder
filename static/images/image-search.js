var appId = '2483710-28f8c0d8555ae721ae5d37cf2';

new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        photos: [],
        totalPhotos: 0,
        perPage: 32,
        currentPage: 1,
        searchQuery: '',
        myImages: [],
        categories: [
            ['fashion', 'Мода'],
            ['nature', 'Природа'],
            ['backgrounds', 'Фон'],
            ['science', 'Наука'],
            ['education', 'Образование'],
            ['people', 'Люди'],
            ['feelings', 'Чувства'],
            ['religion', 'Религия'],
            ['health', 'Здоровье'],
            ['places', 'Места'],
            ['animals', 'Животные'],
            ['industry', 'Индустрия'],
            ['food', 'Еда'],
            ['computer', 'Комьютеры'],
            ['sports', 'Спорт'],
            ['transportation', 'Транспорт'],
            ['travel', 'Путешествия'],
            ['buildings', 'Строения'],
            ['business', 'Бизнес'],
            ['music', 'Музыка']
        ],
        options: {
                params: {
                    key: appId,
                    per_page: this.perPage,
                    page: this.currentPage,
                    q: this.searchQuery,
                    lang: 'ru',
                    order: 'popular',
                    image_type: 'photo',
                    category: ''
                }
            }
    },
    methods: {
        fetchPhotos: function () {
            this.$http.get('https://pixabay.com/api/', this.options).then(function (response) {
                this.photos = response.data.hits;
                this.totalPhotos = parseInt(response.data.total);
            }, console.log);
        },
        searchImage: function () {
            this.options.params.q = this.searchQuery;
            this.fetchPhotos();
        },
        getPrevPage: function () {
            this.currentPage = this.currentPage == 1 ? 1 : this.currentPage - 1;
            this.options.params.page = this.currentPage;
            this.fetchPhotos();
        },
        getNextPage: function () {
            this.currentPage = this.currentPage == this.totalPages ? 1 : this.currentPage + 1;
            this.options.params.page = this.currentPage;
            this.fetchPhotos();
        },
        filterByCategory: function (category) {
            this.options.params.category = category;
            this.fetchPhotos();
        },
        isActiveCategory: function (category) {
            return (category == this.options.params.category) ? true : false;
        },
        addImageToMe: function (url, imageId) {
            this.$http.post(window.location.href, {
                url: url,
                image_id: imageId
            }).then(function () {
                this.myImages.push(imageId);
                swal({
                    position: 'top-end',
                    type: 'success',
                    title: 'Изображение сохранено',
                    showConfirmButton: false,
                    timer: 1500
                })
            }, console.log);
        },
        getMyImages: function () {
            this.$http.get(window.location.href + '?action=get_my_images').then(function (response) {
                console.log(response);
                this.myImages = response.body.my_images;
            }, console.log);
        },
        isInMyImages: function (imageId) {
            return this.myImages.indexOf(imageId) < 0 ? true: false;
        }
    },
    created: function () {
        this.fetchPhotos(this.currentPage);
        this.getMyImages();
    },
    computed: {
        totalPages: function () {
            return Math.ceil(this.totalPhotos / this.perPage);
        }
    }
});
import React from 'react';
import './App.css';

export default class App extends React.Component<any, any> {
  constructor(props: any) {
    super(props);
    this.state = {
      books: [],
      categories: [],
      page: 1,
      sorted_by: 'title',
      order: 'asc'

    };
  }
  componentDidMount(): void {
    this.updateInfo();
  }
  componentDidUpdate(prevProps: Readonly<any>, prevState: Readonly<any>, snapshot?: any): void {
    if (prevState.page !== this.state.page || prevState.sorted_by !== this.state.sorted_by || prevState.order !== this.state.order) {
      this.updateInfo();
    }
  }
  updateInfo = () => {
    const limit = 10;
    const offset = (this.state.page - 1) * limit;
    fetch(`/api/books?limit=${limit}&offset=${offset}&sorted_by=${this.state.sorted_by}&order=${this.state.order}`).then((response) => response.json()).then((data) => {
      this.setState({ books: data });
      console.log(data);
    });
    fetch('/api/categories/').then((response) => response.json()).then((data) => {
      // for (let category of data) {
      //   this.state.categories[category.id] = category.name;
      // }
      // this.setState({});
      // console.log(data);
      this.setState({ categories: data });
    });
  }
  render() {
    return (
      <div className="all_main">
        <div className="categories">
          <div className="add_category">
            <h2>Add category:</h2>
            <input type='text' id='category_name' />
            <button onClick={() => {
              const name = document.getElementById('category_name') as HTMLInputElement;
              console.log(name.value);
              fetch('/api/categories/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: name.value })
              }).then(() => {
                this.updateInfo();
              });
            }}>Add</button>
          </div>
          <table>
            <thead className='theadmini'>
              <th>Name</th>
              <th>Delete</th>
            </thead>
            <tbody className='tbodymini'>
              {this.state.categories.map((category: any) => {
                return (
                  <tr key={category.id}>
                    <th>{category.name}</th>
                    <th><button onClick={() => {
                      fetch(`/api/categories/${category.id}`, {
                        method: 'DELETE',
                      }).then((data: any) => {
                        this.updateInfo();
                      });
                    }}>Delete</button></th>
                  </tr>
                );
              })}

            </tbody>
          </table>

        </div>
        <div className="main">
          <div className="addBook">
            <form action='/api/books' method='POST' onSubmit={(event) => {
              event.preventDefault();
              const form = event.target as HTMLFormElement;
              const data = {
                title: (form.elements.namedItem('title') as HTMLInputElement).value,
                author: (form.elements.namedItem('author') as HTMLInputElement).value,
                category_id: Number((form.elements.namedItem('category_id') as HTMLSelectElement).value)
              };
              console.log(data);
              fetch('/api/books', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
              }).then(() => {
                this.updateInfo();
              });
              }}>
              <h2>Add book:</h2>
              <input type='text' name='title' placeholder='Title' />
              <input type='text' name='author' placeholder='Author' />
              <select name='category_id'>
                {this.state.categories.map((category: any) => {
                  return (
                    <option key={category.id} value={category.id}>{category.name}</option>
                  );
                })}
              </select>
              <button type='submit'>Add</button>
            </form>

          </div>
          <div className="sortby">
            <h2>Sort by:</h2>
            <div>
              <button onClick={() => this.setState({ sorted_by: 'title' })}>Title</button>
              <button onClick={() => this.setState({ sorted_by: 'author' })}>Author</button>
              <button onClick={() => this.setState({ sorted_by: 'category' })}>Category</button>
              <button onClick={() => this.setState({ sorted_by: 'created_at' })}>Created At</button>
              <button onClick={() => this.setState({ sorted_by: 'updated_at' })}>Updated At</button>

            </div>
            <div>
              <button onClick={() => this.setState({ order: 'asc' })}>Asc</button>
              <button onClick={() => this.setState({ order: 'desc' })}>Desc</button>

            </div>
          </div>
          <table>
            <thead>
              <tr>
                <th><h2>title</h2></th>
                <th><h2>author</h2></th>
                <th><h2>category</h2></th>
                <th><h2>Date added</h2></th>
                <th><h2>Date updated</h2></th>
                <th><h2>Confirm</h2></th>
                <th><h2>Delete</h2></th>
              </tr>
            </thead>
            <tbody>
              <tr></tr>
              {this.state.books.map((book: any) => {
                // let title = book.title
                // let author = book.author
                // let category_id = book.category
                return (
                  <tr key={book.id} className='book'>

                    <th><input type='text' name='title' id={`title${book.id}`} value={book.title} onChange={(event) => {
                      // title = event.target.value
                      book.title = event.target.value
                      this.setState({})
                    }} /></th>
                    <th><input type='text' name='author' id={`author${book.id}`} value={book.author} onChange={(event) => {
                      // author = event.target.value
                      book.author = event.target.value
                      this.setState({})
                    }} /></th>
                    <th>
                      <select name='category_id' id={`category${book.id}`} value={book.category_id} onChange={(event) => {
                        book.category_id = event.target.value
                        this.setState({})
                      }}>
                        {this.state.categories.map((category: any) => {
                          return (
                            <option key={category.id} value={category.id}>{category.name}</option>
                          );
                        })}
                      </select>
                    </th>
                    <th>{book.created_at}</th>
                    <th>{book.updated_at}</th>
                    <th><button onClick={() => {
                      const data = {
                        title: book.title,
                        author: book.author,
                        category_id: book.category_id
                      }
                      console.log(data)
                      fetch(`/api/books/${book.id}`, {
                        method: 'PUT',
                        headers: {
                          'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                      }).then(() => {
                        this.updateInfo();
                      }
                      );
                    }
                    }>Confirm</button></th>
                    <th><button onClick={() => {
                      fetch(`/api/books/${book.id}`, {
                        method: 'DELETE',
                      }).then(() => {
                        this.updateInfo();
                      });
                    }}>Delete</button></th>

                  </tr>

                );
              })}
            </tbody>
          </table>
          <div className="pager">
            <button onClick={() => this.setState({ page: Math.max(1, this.state.page - 1) })}>Previous</button>
            <h2>{this.state.page}</h2>
            <button onClick={() => this.setState({ page: this.state.page + 1 })}>Next</button>
          </div >
        </div >
      </div>

    );
  }
}
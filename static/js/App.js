//pass a review as a prop to display its information
function Review(props) {
    return (<div>
        <h3>Movie ID: {props.movieID} </h3>
        <h3>Your Rating: {props.rating}</h3>
        <h3>Your Comment:</h3>
        <h2>{props.comment}</h2>
        <input type="number" onChange={props.onRate} value={props.rating} min="1" max="5"/>
        <input value={props.comment} onChange={props.onEdit}/>
        <button onClick={props.onDelete}>Delete</button>
    </div>);
}

function App() {
  //val is a refrence to our variable and setVal is a function to change all arguments using the name "val"
    const[val, setVal] = React.useState([])

    function handleDelete(i) {
      setVal([...val.slice(0, i), ...val.slice(i+1)]);
    }
  
    function handleRatingChange(i, e) {
      const newReviews = val.slice();
      newReviews[i].rating = e.target.value;
      setVal(newReviews);
    }
  
    function handleCommentChange(i, e) {
      const newReviews = val.slice();
      newReviews[i].comment = e.target.value;
      setVal(newReviews);
    }


      //Posts review changes back to 'save_reviews' route
      function onClickSave() {
        fetch('/save_reviews', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          //makes sure the request body is of the same datatype as declared in headers
          body: JSON.stringify(val),
        })
          //changes response object to json
          .then((response) => response.json());
      }
      
      //in order to generate all reviews that we have, we use .map()
      const reviews = val.map(
        //for all reviews in array of reviews (i), turn each review into a prop able to be passed to Review component
        (review, i) => <Review 
          //maps review attributes to new prop attributes
          movieID={review.movie_id}
          rating={review.rating}
          comment={review.comment}
          //functions applicable to the component
          onDelete={() => handleDelete(i)}
          onEdit={(e) => handleCommentChange(i, e)}
          onRate={(e) => handleRatingChange(i, e)}
        />);
      
      //get reviews as API response
      React.useEffect(() => {
        fetch('/get_reviews', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        })
        //converts response to JSON object and sets val to data recieved
          .then((response) => response.json())
          .then((data) => {
            setVal(data);
          });
      }, []);

    return (
        <div className="App">
            {reviews}
            <button onClick={onClickSave}>Save Changes</button>
        </div>
    )
}

const domContainer = document.querySelector('#react_app');
ReactDOM.render(React.createElement(App), domContainer);

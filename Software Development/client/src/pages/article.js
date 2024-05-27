import React from 'react';

const Article = ({ name, desc, image}) => {
    return (
        <div>
            <img src={image} />
            <h1>{name}</h1>
            <p>{desc}</p>
        </div>
    );
}

export default Article;
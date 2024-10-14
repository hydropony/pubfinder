import React, { useState, useEffect} from 'react';

const Filter = ({name}) => {
  const [isSelected, setIsSelected] = useState(false)
  return (
    <button className='border border-slate-500 text-2xl rounded-md p-1 border-2' onClick={() => setIsSelected(!isSelected)}>
      {name} {isSelected === true ? "❌" : ""}
    </button>
  )
}

const SearchResult = ({name, rating, setDetailedName}) => {
  return (
    <li key={name}><button onClick={() => {setDetailedName(name);console.log("clicked")}} className="bg-gray-700 text-7xl font-bold m-1">{name} {rating}⭐</button></li>
  )
}

function App() {
  const [jsonData, setJsonData] = useState(null)
  const [detailedName, setDetailedName] = useState(null)

  const getPubByIndex = (index) => {
    return {
      name: jsonData.name[index],
      address: jsonData.address[index],
      place_id: jsonData.place_id[index],
      rating: jsonData.rating[index],
      total_ratings: jsonData.total_ratings[index],
      reviews: jsonData.reviews[index],
    }
  }

  useEffect(() => {
    fetch('../Helsinki_pubs_reviews.json')
    .then(response => response.json())
    .then(data => {
      console.log(data.name[0]); // Access your JSON data here
      setJsonData(data)
      // console.log(Object.values(data.rating)[0])
    })
    .catch(error => {
      console.error('Error loading JSON:', error);
    });

    // Set the tab name (document title) when the component mounts
    document.title = "Pubfinder";
    // Function to change the favicon dynamically
    const changeFavicon = (faviconURL) => {
      const link = document.querySelector("link[rel*='icon']") || document.createElement('link');
      link.type = 'image/x-icon';
      link.rel = 'shortcut icon';
      link.href = faviconURL;
      document.getElementsByTagName('head')[0].appendChild(link);
    };

    // Set the favicon when the component mounts
    changeFavicon('../icons8-beer-48.png');
  }, []);

  const Detailed = ({name, setDetailedName}) => {
    if (jsonData === null) {
      console.log('jsondata null')
      return
    }
    if (name === null) {
      console.log('detailedname null')
      return
    }
    const index = Object.entries(jsonData.name).filter(entry => entry[1] === name)[0][0]
    // console.log(index)
    const pub = getPubByIndex(index)
  
    return (
      <div className='bg-gray-300 min-h-screen text-4xl p-2'>
        <ul>
          <li><h1 className='font-bold text-'>{pub.name} {pub.rating}⭐</h1></li>
          <li><h3>Total reviews: {pub.total_ratings}</h3></li>
          <li><h3>Text reviews analyzed by us: {pub.reviews.length}</h3></li>
          <li><a className='hover:text-slate-700' target='_blank' href={'https://www.google.com/maps/place/?q=place_id:' + pub.place_id}>Address: {pub.address}</a></li>
          <li><button onClick={() => setDetailedName(null)} className='border border-2 border-slate-500 rounded-md p-1 my-2'>Return</button></li>
        </ul>
      </div>
    )
  }

  return (
    <div>
      <div className='bg-gray-700 text-white text-4xl p-4 font-bold'>Pubfinder🍺</div>
      <div className={detailedName === null ? 'visible' : 'hidden'}>
        <div className='bg-gray-400'>
          <div className='p-4 flex text-2xl justify-evenly font-medium'>
            Filters:
            <Filter name="Beer🍺"></Filter>
            <Filter name="Wine🍷"></Filter>
            <Filter name="Cocktails🍸"></Filter>
            <Filter name="Shots🥃"></Filter>
            <Filter name="Dance💃"></Filter>
            <Filter name="Rock🤘"></Filter>
            <Filter name="Hip-hop😎"></Filter>
            <Filter name="Pop🎵"></Filter>
            <Filter name="Bar🥂"></Filter>
            <Filter name="Club🪩"></Filter>
            <Filter name="Pet-friendly🐕"></Filter>
          </div>
        </div>
        <div className='bg-gray-300 text-3xl font-bold p-4'>Search results:</div>
        <div className="bg-gray-300 text-white min-h-screen flex items-center justify-center">
          <ul>
            {jsonData === null ? "" : Object.keys(jsonData.name).map(index => getPubByIndex(index)).sort((a, b) => b.rating - a.rating).map(pub => <SearchResult name={pub.name} rating={pub.rating} key={pub.name} setDetailedName={setDetailedName}></SearchResult>)}
          </ul>
        </div>
      </div>
      <Detailed name={detailedName} setDetailedName={setDetailedName}></Detailed>
    </div>
  );
}

export default App;
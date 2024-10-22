import React, { useState, useEffect} from 'react';
import WordCloud from 'react-d3-cloud';

const Filter = ({name, index, setFilters, filters}) => {
  const [isSelected, setIsSelected] = useState(false)
  const onclick = () => {
    setIsSelected(!isSelected)
    let copiedarray = [...filters]
    copiedarray[index] = !copiedarray[index]
    setFilters(copiedarray)
  }
  return (
    <button className='border border-slate-500 text-2xl rounded-md p-1 border-2' onClick={onclick}>
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
  const [filters, setFilters] = useState([false, false, false, false, false, false, false, false, false, false, ])

  const compare = (a, b) => {
    let sum = 0
    for (let i = 0; i < 10; i++) {
      if (filters[i])
        sum += b.categories[i] - a.categories[i]
    }
    return sum + (b.rating - a.rating) / 20//+ (b.reviews.length - a.reviews.length) / (b.reviews.length + a.reviews.length) // (b.rating - a.rating) / 5
  }

  const threshold = (pub) => {
    for (let i = 0; i < 10; i++) {
      if (filters[i]) {
        if (pub.categories[i] < 0.15) {
          return false
        }
      }
    }
    return true
  }

  const getPubByIndex = (index) => {
    return {
      name: jsonData.name[index],
      address: jsonData.address[index],
      place_id: jsonData.place_id[index],
      rating: jsonData.rating[index],
      total_ratings: jsonData.total_ratings[index],
      reviews: jsonData.reviews[index],
      categories: jsonData.categories[index]
    }
  }

  useEffect(() => {
    fetch('../pubs_and_categories.json')
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

    function countWordFrequencies(text) {
      // Step 1: Convert text to lowercase and split into words
      let words = text.toLowerCase()
                      .replace(/[^\w\s]/g, '')  // Remove punctuation
                      .split(/\s+/);            // Split by whitespace
  
      // Step 2: Create an object to store word frequencies
      let wordFrequencies = {};
  
      words.forEach(word => {
          if (word in wordFrequencies) {
              wordFrequencies[word] += 1;
          } else {
              wordFrequencies[word] = 1;
          }
      });

      const ret = []
      Object.keys(wordFrequencies).forEach(function(key, value) {
        ret.push({text: key, value: wordFrequencies[key]})
      });
      console.log(ret)
      return ret;
    }

    const data = [
      { text: 'Hey', value: 1000 },
      { text: 'lol', value: 200 },
      { text: 'first impression', value: 800 },
      { text: 'very cool', value: 1000000 },
      { text: 'duck', value: 10 },
    ];

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
          {/* {pub.categories.map(score => <li><h3>{score}</h3></li>)} */}
          {/* <WordCloud data={countWordFrequencies(pub.reviews.join(" "))}></WordCloud> */}
          <li>
            <div className='m-4 size-1/2'>
              <WordCloud data={countWordFrequencies(pub.reviews.join(" "))} fontSize={(d) => Math.log(d.value) * 50} rotate={0}></WordCloud>
            </div>
          </li>
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
            <Filter name="Beer🍺" index={0} setFilters={setFilters} filters={filters}></Filter>
            <Filter name="Food" index={1} setFilters={setFilters} filters={filters}></Filter>
            <Filter name="Cocktails🍸" index={2} setFilters={setFilters} filters={filters}></Filter>
            <Filter name="Karaoke" index={3} setFilters={setFilters} filters={filters}></Filter>
            <Filter name="Games💃" index={4} setFilters={setFilters} filters={filters}></Filter>
            <Filter name="Burgers" index={5} setFilters={setFilters} filters={filters}></Filter>
            <Filter name="Club" index={6} setFilters={setFilters} filters={filters}></Filter>
            <Filter name="Pop🎵" index={7} setFilters={setFilters} filters={filters}></Filter>
            <Filter name="Bar🥂" index={8} setFilters={setFilters} filters={filters}></Filter>
            <Filter name="Club🪩" index={9} setFilters={setFilters} filters={filters}></Filter>
            <Filter name="Pet-friendly🐕"></Filter>
          </div>
        </div>
        <div className='bg-gray-300 text-3xl font-bold p-4'>Search results:</div>
        <div className="bg-gray-300 text-white min-h-screen flex items-center justify-center">
          <ul>
            {jsonData === null ? "" : Object.keys(jsonData.name).map(index => getPubByIndex(index)).filter(pub => threshold(pub)).sort((a, b) => compare(a, b)).map(pub => <SearchResult name={pub.name} rating={pub.rating} key={pub.name} setDetailedName={setDetailedName}></SearchResult>)}
          </ul>
        </div>
      </div>
      <Detailed name={detailedName} setDetailedName={setDetailedName}></Detailed>
    </div>
  );
}

export default App;
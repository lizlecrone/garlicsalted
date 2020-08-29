function Advancement({selected, toggle, icon, title, description}) {
	return (
		<div
		    onClick={toggle}
			style={{
				cursor: toggle ? 'pointer' : '',
				fontFamily: 'MinecraftiaRegular',
				backgroundColor: selected ? '#202020' : 'gray',
				border: '4px solid #555555',
				borderRadius: '4px',
				display: 'flex',
				alignItems: 'center',
				margin: '4px',
				padding: '4px 0',
			}}
		>
			<div>
				<img
					src={`/static/${icon}`}
					style={{
						width:'2em',
						imageRendering: 'pixelated',
						margin: '0 1em',
					}}
				/>
			</div>
			<div>
				<div
					style={{
						color:'yellow',
					}}
				>
					{title}
				</div>
				<div
					style={{
						color:'white',
					}}
				>
					{description}
				</div>
			</div>
			{toggle ? (
				<div style={{margin: '4px 1em 4px auto'}}>
				    <input
				   		type="checkbox"
				   		checked={selected}
				   		style={{cursor: 'pointer'}}
				   		readOnly
			   		/>
				</div>
				)
				: null
			}
		</div>

	)
}

function Button({enabled, onClick, children, color}) {

	return (
		<button
			disabled={!enabled}
			style={{
				cursor: enabled ? 'pointer' : '',
				backgroundColor: enabled ? color || 'green' : '#2d2c2d',
				color: enabled ? 'white' : '#848484',
				fontFamily: 'MinecraftiaRegular',
				padding: '.75em',
				margin: '15px',
				width: '300px',
				borderRadius: '5px',
				alignSelf: 'center',
			}}
			onClick={onClick}
		>
			{children}
		</button>
	)
}

function Footer({enabled, onClick, number}) {
	return(
		<div
			style={{
				width: '100%',
				display: 'flex',
				position: 'sticky',
				bottom: 0,
				justifyContent: 'center',
				backgroundImage: 'url("/static/bg.png")',
				backgroundRepeat: 'repeat',
			}}
		>
			<span
				style={{
					alignSelf: 'center',
					color: 'white',
					fontFamily: 'MinecraftiaRegular',
				}}
			>
				{number} selected
			</span>
			<Button
				enabled={enabled}
				onClick={onClick}
			>
				Download
			</Button>
		</div>
	)
}

function Header({children}) {
	return(
		<div
			style={{
				width: '100%',
				display: 'flex',
				position: 'sticky',
				top: 0,
				justifyContent: 'center',
				backgroundImage: 'url("/static/bg.png")',
				backgroundRepeat: 'repeat',
			}}
		>
			{children}
		</div>
	)
}

function Customize () {
	const [advancements, setAdvancements] = React.useState(null)
	const [selected, setSelected] = React.useState([])
	const [enabled, setEnabled] = React.useState(false)

	function getAdvancements () {
		axios.get('/api/advancements')
			.then(response => {
				setAdvancements(response.data)
			})
	}

	React.useEffect(getAdvancements, [])

	if (advancements === null) {
		return null
	}

	function handleToggle(id) {

		let newSelected
		if (selected.includes(id)) {
			newSelected = selected.filter(s => id !== s)
		} else {
			newSelected = [...selected, id]
		}

		setSelected(newSelected)
		setEnabled(newSelected.length > 0)
	}

	function handleDownload() {
		setEnabled(false)
		const selectedJson = JSON.stringify(selected)
		const zipPath = `/generate/custom?selected=${selectedJson}`
		window.open(zipPath)
	}


	return (
		<div
			style={{
				display: 'flex',
				flexDirection: 'column',
			}}
		>
			<p style={{
				color: 'white',
				fontFamily: 'MinecraftiaRegular',
				padding: '24px',
			}}>
				Select which advancements to include.
			</p>
			{advancements.map(e => (
				<Advancement
					key={e.id}
					icon={e.icon}
					title={e.title}
					description={e.description}
					selected={selected.includes(e.id)}
					toggle={() => {handleToggle(e.id);}}
				/>
			))}
			<Footer
				enabled={enabled}
				number={selected.length}
				onClick={handleDownload}
			/>
		</div>
	)
}

function Randomize () {

	function handleRandomDownload() {
		const zipPath = '/generate/random'
		window.open(zipPath)
	}

	return(
		<div>
			<p style={{
				color: 'white',
				fontFamily: 'MinecraftiaRegular',
				padding: '24px',
			}}>
				Race to complete 5 random advancements!
			</p>
			{
				[...Array(5)].map((e, i) => (
					<Advancement
						key={i}
						icon='question_block.jpg'
						title='???'
						description='??????'
						selected
					/>
				))
			}
			
			<Footer
				enabled
				number={5}
				onClick={handleRandomDownload}
			/>
		</div>
	)
}

function Instructions() {
	return (
		<div style={{
			color: 'white',
			fontFamily: 'MinecraftiaRegular',
			padding: '24px',
		}}>
		<h4>
		    What is this?
	    </h4>
	    <p>
		    Start a new world with custom advancements and race alone or with friends to complete them all!
		    The custom advancements will show up in your advancements menu. When you complete them all,
		    your victory will be announced in chat and you'll be put into spectator mode.
		</p>
		<h4>
		    How do I use it?
	    </h4>
	    <p>
		    No mods necessary!
	    </p>

		<ol>
			<li>Select Randomize or Customize to build a data pack.</li>
			<li>Download it.</li>
			<li>Unzip it in your Minecraft world's "datapacks" folder</li>
			<li>Run "/function bingo:start" when all players are online and ready!</li>
		</ol>
		</div>
	)
}

function App () {
	const LOC_MENU = 'menu'
	const LOC_RANDOMIZE = 'randomize'
	const LOC_CUSTOMIZE = 'customize'

	const [location, setLocation] = React.useState(LOC_MENU)

	function handleShowCustomize() {
		setLocation(LOC_CUSTOMIZE)
	}

	function handleShowRandomize() {
		setLocation(LOC_RANDOMIZE)
	}

	function handleBack() {
		setLocation(LOC_MENU)
	}

	return (
		<div style={{
			minHeight: '100%',
			backgroundImage: 'url("/static/bg.png")',
			backgroundRepeat: 'repeat',
			display: 'flex',
			flexDirection: 'column',
			alignItems: 'center',
		}}>
			<Header>
				{location === LOC_MENU ? (
					<React.Fragment>
						<Button
						    key="randomize"
							enabled
							onClick={handleShowRandomize}
						>
							Randomize
						</Button>
						<Button
							key="customize"
							enabled
							onClick={handleShowCustomize}
						>
							Customize
						</Button>
					</React.Fragment>
				) : (
					<Button
						key="back"
						enabled
						color='#6b6b6b'
						onClick={handleBack}
					>
						Back
					</Button>
				)}

			</Header>
			<div
				style={{
					maxWidth: '1000px',
				}}
			>
				{location === LOC_MENU ? <Instructions /> : null}
				{location === LOC_CUSTOMIZE ? <Customize /> : null}
				{location === LOC_RANDOMIZE ? <Randomize /> : null}
			</div>
		</div>
	)
}


ReactDOM.render(<App />, document.querySelector('#app'))


import { Link } from "react-router-dom";

const Home = () => {
    return (
        <div className="hero min-h-screen bg-base-200">
          <div className="hero-content flex-col lg:flex-row-reverse">
              <div>
                  <h1 className="text-5xl font-bold">Witaj w systemie MARTIAL.AI!</h1>
                  <p className="py-6">
                      Zaloguj się, aby korzystać z systemu. Jeśli nie masz konta, skontaktuj się z administratorem.
                  </p>
                  <Link to="/login" className="btn btn-primary">Zaloguj się</Link>
              </div>
          </div>
      </div>
    )
    
}

export default Home
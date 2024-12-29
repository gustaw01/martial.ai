import { Link } from "react-router-dom";

const Login = () => {
    return (
        <section className="hero min-h-screen bg-base-200">
            <div className="hero-content flex-col lg:flex-row-reverse">
                <div className="text-center lg:text-center">
                    <h1 className="text-5xl font-bold">Zaloguj się</h1>
                </div>
                <div className="card shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
                    <form className="card-body">
                        <div className="form-control center">
                            <label className="label">
                                <span className="label-text">Email</span>
                            </label><br />
                            <input type="email" placeholder="email" className="input input-bordered" required/>
                        </div>
                        <div className="form-control center">
                            <label className="label">
                                <span className="label-text">Password</span>
                            </label><br />
                            <input type="password" placeholder="password" className="input input-bordered" required/>
                            <br />
                            <label className="label">
                                <a href="#" className="label-text-alt link link-hover">Zapomniałeś hasła?</a>
                            </label>
                        </div>
                        <div className="form-control center">
                            <Link to="/dash">
                                <button className="btn btn-primary">
                                    Login
                                </button>
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </section>
    )
}
export default Login
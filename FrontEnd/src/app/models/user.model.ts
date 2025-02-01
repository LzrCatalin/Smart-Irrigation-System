export class User {
    id: string | undefined;
    email: string | undefined;

    constructor(id: string, email: string) {
        this.id = id;
        this.email = email;
    }
}
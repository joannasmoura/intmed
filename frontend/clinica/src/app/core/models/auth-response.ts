import { User } from './user';

export interface AuthResponse {  
    access: string,
    refresh: string,
    user: User
}